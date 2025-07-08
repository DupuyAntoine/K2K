from agents.model.model import Model

class NoAgent:
    def __init__(self, model):
      self.model = Model(model_name=model)

    def generate_response(self, context, query):
      prompt = (
         "Contexte : {context}"
         "Requête : {query}"
      ).format(query = query, context = context)
      response = self.model.generate(prompt)
      return response
