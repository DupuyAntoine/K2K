import os
import json
import logging
import re
import requests
from groq import Groq # type: ignore

logger = logging.getLogger(__name__)

class DataIdentificationAgent:
  def __init__(self):
    self.client = Groq(api_key=os.environ["GROQ_API_KEY"])
    self.model = "compound-beta"  # ou "compound-beta-mini" si tu veux une recherche légère

  def extract_criteria(self, analysis_text):
    logger.info("Extraction des critères depuis l'analyse...")
    prompt = (
      "Extract key criteria as JSON: theme, period, location, source, format.\n"
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

  def build_query(self, criteria):
    base = f"{criteria.get('theme','')} {criteria.get('location','')} {criteria.get('period','')}".strip()
    fmt = (criteria.get('format') or '').strip().lower()
    known_formats = {"csv", "json", "netcdf", "xml", "zip", "txt", "xls", "xlsx", "geojson"}
    query = base
    if fmt in known_formats:
      query += f" filetype:{fmt}"
    return query

  # TODO: check google search api documentation to select only files and if not possible filter results
  def search_datasets_with_serpapi(self, query, num_results=10):
    
    logger.info("Var env dispos: %s", str(os.environ))

    serp_api_key = os.environ["SERP_API_KEY"]

    logger.info("Lancement de la recherche via SerpAPI: %s", serp_api_key)
    
    if not serp_api_key:
      logger.error("Clé API SerpAPI manquante.")
      return []

    logger.info(f"Recherche via SerpAPI: {query}")

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

        # On filtre uniquement les formats utiles
        if any(ext in link.lower() for ext in [".csv", ".json", ".nc", ".zip", ".xls", ".xlsx", ".geojson", ".txt"]):
          datasets.append({
            "title": title,
            "url": link,
            "description": snippet
          })

      return datasets

    except Exception as e:
      logger.error(f"Erreur lors de la requête SerpAPI : {e}")
      return []

  def search_datasets(self, criteria):
    query = self.build_query(criteria)
    logger.info("Requête construite pour la recherche de datasets : %s", query)
    results = self.search_datasets_with_serpapi(query)
    logger.info("Résultats trouvés via SerpAPI : %s", str(results))
    return self.filter_results(results)

  def filter_results(self, results):
    seen = set()
    filtered = []

    valid_exts = {".csv", ".json", ".nc", ".zip", ".xls", ".xlsx", ".geojson", ".txt"}

    for r in results:
      url = r.get("url", "").strip()
      title = r.get("title", "").strip()
      description = r.get("description", "").strip()

      if not url or url in seen:
          continue
      seen.add(url)

      if any(ext in url.lower() for ext in valid_exts):
        filtered.append({
          "title": title,
          "description": description,
          "url": url
        })
      else:
        logger.info(f"URL ignorée (format inconnu) : {url}")

    logger.info("Résultats filtrés : %d fichier(s) trouvé(s)", len(filtered))
    logger.debug("Résultats filtrés (contenu): %s", json.dumps(filtered, indent=2, ensure_ascii=False))

    return filtered

  def identify_datasets(self, analysis):
    criteria = self.extract_criteria(analysis)
    return self.search_datasets(criteria)
