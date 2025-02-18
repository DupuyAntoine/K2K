from agents.model.model import Model

class ResponseAgent:
  def __init__(self, model):
    self.model = Model(model_name=model)

  def construct_response(self, data_results):
    prompt = (
      "Tu es un agent chargé de formater les réponses. À partir des "
      "données suivantes : '{}', assemble une réponse claire composée "
      "de la liste des jeux de données et les fichiers associés sélectionnés et justifie pourquoi "
      "ces jeux de données ont été recommandés particulièrement."
      "N'invente pas des jeux de données hors de ce qui t'a été transmis."
    ).format(data_results)
    response = self.model.generate(prompt)
    return response
