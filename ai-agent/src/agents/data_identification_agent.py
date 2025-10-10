import os
import json
import logging
import re
import requests
from bert_score import score
from deep_translator import GoogleTranslator # type: ignore
from groq import Groq  # type: ignore

logger = logging.getLogger(__name__)


class OpenDataRetriever:
  """Recherche multi-source sur les principaux portails open data mondiaux."""

  SOURCES = {
    "data_gouv": "https://www.data.gouv.fr/api/1/datasets/",
    "data_gov": "https://catalog.data.gov/api/3/action/package_search",
    "opendatasoft": "https://public.opendatasoft.com/api/v2/catalog/datasets",
  }

  def search_all_sources(self, criteria, limit_per_source=10):
    all_results = []
    for source, url in self.SOURCES.items():
      try:
        base_query, params = self._build_query_for_source(source, criteria)
        logger.info(f"[{source}] Requête : {url} query={base_query} params={params}")
        r = requests.get(url, params=params, timeout=10, headers={"Accept": "application/json"})
        if r.status_code != 200:
          logger.warning(f"[{source}] HTTP {r.status_code}")
          continue
        data = r.json()
        parsed = self._parse_results(source, data, limit_per_source)
        logger.info(f"Results for {source} : {parsed}")
        all_results.extend(parsed)
      except Exception as e:
        logger.error(f"[{source}] Erreur : {e}")
    return all_results

  # ======================= Construction requête large =======================

  def _build_query_for_source(self, source, criteria):
    theme = criteria.get("theme")

    if source in {"data_gouv", "opendatasoft"}:
      try:
        theme = GoogleTranslator(source="auto", target="fr").translate(theme)
        logger.info(f"Requête traduite : {theme}")
      except Exception as e:
        logger.warning(f"Erreur traduction du thème : {e}")

    base_query = theme.strip()

    if source == "data_gouv":
      params = {"q": base_query, "page_size": 10}
    elif source == "data_gov":
      params = {"q": base_query, "rows": 10, "sort": "score desc"}
    elif source == "opendatasoft":
      params = {"search": base_query, "rows": 10}
    else:
      params = {"q": base_query}

    return base_query, params

  # ======================= Parsing par API =======================

  def _parse_results(self, source, data, limit):
    results = []
    try:
      if source == "data_gouv":
        for d in data.get("data", [])[:limit]:
          res = d.get("resources", [])
          res_url = res[0].get("url") if res else d.get("url") or d.get("landingPage")
          results.append({
            "title": d.get("title"),
            "description": d.get("description"),
            "url": res_url,
            "source": "data.gouv.fr"
          })

      elif source == "data_gov":
        for d in data.get("result", {}).get("results", [])[:limit]:
          res = d.get("resources", [])
          res_url = res[0].get("url") if res else d.get("url") or d.get("landingPage")
          results.append({
            "title": d.get("title"),
            "description": d.get("notes"),
            "url": res_url,
            "source": "data.gov"
          })

      elif source == "opendatasoft":
        for d in data.get("datasets", [])[:limit]:
          links = d.get("links", [])
          res_url = links[0].get("href") if links else d.get("url")
          meta = d.get("metas").get("dublin-core")
          results.append({
            "title": meta.get("title"),
            "description": meta.get("description"),
            "url": res_url,
            "source": "OpenDataSoft"
          })

    except Exception as e:
      logger.error(f"Erreur parsing {source}: {e}")

    return results

  # ======================= BERTScore =======================

  def compute_bertscore(self, candidates, reference, lang="en"):
    try:
      P, R, F1 = score(candidates, [reference] * len(candidates), lang=lang)
      return F1.tolist()
    except Exception as e:
      logger.error(f"Erreur calcul BERTScore : {e}")
      return [0.0] * len(candidates)

  def semantic_filter(self, results, criteria, top_k=10):
    if not results:
      return []

    # On concatène tous les critères disponibles pour former la "requête de référence"
    reference = " ".join(
      str(criteria.get(k, "")) for k in
      ["theme", "location", "period", "producer", "format"]
      if criteria.get(k)
    ).strip()

    if not reference:
      reference = "general dataset"

    candidates = [
      f"{r.get('title', '')} {r.get('description', '')}" for r in results
    ]

    scores = self.compute_bertscore(candidates, reference)
    ranked = sorted(zip(results, scores), key=lambda x: x[1], reverse=True)

    filtered = [{
      "title": r["title"],
      "description": r["description"],
      "url": r["url"],
      "semantic_score": s
    } for r, s in ranked[:top_k]]

    logger.info(f"Filtrage sémantique BERTScore terminé ({len(filtered)} résultats gardés)")
    return filtered

  # ======================= Fallback SerpAPI =======================

  def search_datasets_with_serpapi(self, query, num_results=10):
    serp_api_key = os.environ.get("SERP_API_KEY")
    if not serp_api_key:
      logger.error("Clé API SerpAPI manquante.")
      return []

    logger.info(f"Fallback SerpAPI activé pour : {query}")

    url = "https://serpapi.com/search"
    params = {
      "q": query,
      "api_key": serp_api_key,
      "engine": "google",
      "num": num_results
    }

    try:
      response = requests.get(url, params=params)
      data = response.json()
      results = data.get("organic_results", [])
      datasets = []

      for result in results:
        title = result.get("title", "")
        link = result.get("link", "")
        snippet = result.get("snippet", "")
        if any(ext in link.lower() for ext in
               [".csv", ".json", ".nc", ".zip", ".xls", ".xlsx", ".geojson", ".txt"]):
          datasets.append({
            "title": title,
            "url": link,
            "description": snippet
          })

      return datasets

    except Exception as e:
      logger.error(f"Erreur SerpAPI : {e}")
      return []

  # ======================= Recherche complète =======================

  def retrieve(self, criteria):
    logger.info("Démarrage recherche multi-portails open data...")
    raw_results = self.search_all_sources(criteria)

    if not raw_results:
      theme = criteria.get("theme", "open data")
      logger.warning("Aucun résultat trouvé sur les portails open data. Fallback SERPAPI.")
      raw_results = self.search_datasets_with_serpapi(theme)

    filtered = self.semantic_filter(raw_results, criteria, top_k=10)
    return filtered

class DataIdentificationAgent:
  def __init__(self):
    self.client = Groq(api_key=os.environ["GROQ_API_KEY"])
    self.model = "compound-beta"
    self.opendata_retriever = OpenDataRetriever()

  def extract_criteria(self, analysis_text):
    logger.info("Extraction des critères depuis l'analyse...")
    prompt = (
      "Extract key criteria as JSON: theme, period, location, source, format, producer, user_need, others.\n"
      "Return only a valid JSON object.\n"
      f"Content:\n{analysis_text}"
    )

    response = self.client.chat.completions.create(
      model=self.model,
      messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content
    logger.info("Contenu brut de la réponse : %s", content)

    try:
      return json.loads(content)
    except Exception:
      logger.warning("JSON malformé, tentative de nettoyage...")
      match = re.search(r"\{.*\}", content, re.DOTALL)
      if match:
        try:
          cleaned = match.group(0)
          return json.loads(cleaned)
        except Exception as e2:
          logger.error("Échec même après nettoyage : %s", e2)
      else:
        logger.error("Aucun JSON détecté dans la réponse.")
    return {}

  def identify_datasets(self, analysis):
    criteria = self.extract_criteria(analysis)
    return self.opendata_retriever.retrieve(criteria)
