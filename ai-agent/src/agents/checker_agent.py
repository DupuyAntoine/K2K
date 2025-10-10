import json
import logging
import re
from typing import List, Dict, Any, Optional
from agents.model.model import Model

logger = logging.getLogger(__name__)

class ResponseCheckerAgent:
  """
  Vérifie la cohérence factuelle entre :
    - la requête utilisateur
    - l'analyse du Request Analyst Agent
    - les datasets récupérés
    - la réponse produite par le Response Construction Agent

  Adapte ensuite la réponse finale en fonction du niveau de cohérence.
  """

  def __init__(self, model: str):
    self.model = Model(model_name=model)

  def _build_prompt(
    self,
    query: str,
    system_response: str,
    analysis: str,
    datasets: List[Dict[str, Any]]
  ) -> str:
    """
    Construit le prompt envoyé au modèle.
    """
    prompt = (
      "You are the Response Checker Agent in a conversational dataset search system.\n"
      "Your job is to verify that the system response is factually correct and well-aligned "
      "with the user query, the request analysis, and the dataset metadata.\n\n"
      "--- INPUTS ---\n"
      f"User Query:\n{query}\n\n"
      f"Request Analysis (from analyst agent):\n{analysis}\n\n"
      f"System Response (to check):\n{system_response}\n\n"
      f"Retrieved Datasets:\n{json.dumps(datasets, ensure_ascii=False, indent=2)}\n\n"
      "--- TASK ---\n"
      "1. Identify factual statements in the system response.\n"
      "2. Check each statement against both the request analysis and the dataset metadata.\n"
      "3. Mark each as SUPPORTED or UNSUPPORTED, with a short explanation.\n"
      "4. Assign an overall consistency level: High, Medium, or Low.\n"
      "   - High → All claims supported, no changes needed.\n"
      "   - Medium → Mostly supported but some uncertainty → keep response but add disclaimer.\n"
      "   - Low → Several unsupported claims → rewrite response keeping only supported facts.\n\n"
      "5. Provide the adapted final_response for the user.\n\n"
      "--- OUTPUT FORMAT ---\n"
      "Return a JSON object with keys:\n"
      "{\n"
      "  'consistency': 'High' | 'Medium' | 'Low',\n"
      "  'supported_statements': [ ... ],\n"
      "  'unsupported_statements': [ ... ],\n"
      "  'final_response': '...'\n"
      "}\n"
    )
    return prompt

  def check_response(
    self,
    query: str,
    system_response: str,
    analysis: str,
    retrieved_datasets: List[Dict[str, Any]]
  ) -> Dict[str, Any]:
    """
    Vérifie la réponse.
    Retourne un dictionnaire JSON (déjà parsé).
    """
    prompt = self._build_prompt(query, system_response, analysis, retrieved_datasets)
    raw_output = self.model.generate(prompt)

    try:
      parsed = json.loads(raw_output)
      logger.info(parsed)
    except Exception:
      # fallback si le modèle ne renvoie pas un JSON valide
      logger.warning("JSON malformé, tentative de nettoyage...")

      match = re.search(r"\{.*\}", raw_output, re.DOTALL)
      if match:
        try:
          cleaned = match.group(0)
          parsed = json.loads(cleaned)
          logger.info(parsed)
        except Exception as e2:
          logger.error("Échec même après nettoyage : %s", e2)
          return system_response
      else:
        logger.error("Aucun JSON détecté dans la réponse.")
    return parsed
