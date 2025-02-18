from agents.model.model import Model

class InteractionAgent:
  def __init__(self, model):
    self.model = Model(model_name=model)

  def process_query(self, user_query):
    prompt = (
      "Tu es un assistant intelligent. Ton rôle est d'inciter "
      "l'utilisateur à préciser sa requête au système. "
      "Cette tâche nécessite trois étapes: "
      "1- Analyse la requête suivante : '{}', "
      "2- Si des informations essentielles manquent (exemple : "
      "localisation, format des données, critères de qualité, "
      "objectifs d'utilisation, etc.), génère des questions pour "
      "demander ces informations à l'utilisateur de manière claire et "
      "concise."
      "3- Extrait les éléments importants pour les donner en paramètre à "
      "l'agent de création de requêtes SPARQL."
    ).format(user_query)
    response = self.model.generate(prompt)
    return response
