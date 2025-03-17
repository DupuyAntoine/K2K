from agents.model.model import Model

class InteractionAgent:
  def __init__(self, model):
    self.model = Model(model_name=model)

  def process_query(self, user_query, data_model):
    prompt = (
      "Tu es un assistant de recherche de données. Ton rôle est d'inciter "
      "l'utilisateur à préciser sa requête au système et le guider dans sa recherche. "
      "Cette tâche nécessite plusieurs étapes: "
      "1- Analyse la requête suivante : '{query}', "
      "2- Détection de critères manquants en fonction du modèle de donnée : {data_model}"
      "3- Extrait les critères de recherche de l'utilisateur."
      "Si sa requête est incomplète, tu lui poses des questions pour affiner sa recherche, "
      "sinon tu lui récapitules ses critères et lui demande confirmation."
    ).format(query = user_query, data_model = data_model)
    response = self.model.generate(prompt)
    return response
