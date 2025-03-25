from agents.model.model import Model

class InteractionAgent:
  def __init__(self, model):
    self.model = Model(model_name=model)
    self.context = []
    self.graph = None

  def process_query(self, user_query, data_model = None):
    if not self.graph:
      self.graph = data_model
    self.context.append(user_query)
    prompt = (
      "🧠 **Assistant de recherche intelligent**\n\n"
      "Tu es un assistant spécialisé dans la recherche de données. "
      "Ton objectif est d’aider l'utilisateur à affiner sa requête en fonction du modèle de données disponible. "
      "Tu dois le guider avec des questions pertinentes si sa requête est incomplète ou lui récapituler ses critères pour validation.\n\n"
      
      "🔍 **Analyse de la requête** :\n"
      "👉 Requête utilisateur : '{query}'\n"
      "👉 Modèle de données : {data_model}\n"
      "👉 Contexte du dialogue : {context}\n"

      "📌 **Processus d’assistance** :\n"
      "1️⃣ **Déterminer les informations fournies** : Quels critères sont déjà mentionnés ?\n"
      "2️⃣ **Identifier les critères manquants** en comparant la requête au modèle de données.\n"
      "3️⃣ **Si la requête est incomplète**, poser des questions ciblées pour clarifier les attentes de l'utilisateur.\n"
      "4️⃣ **Si la requête est complète**, récapituler les critères extraits et demander confirmation.\n\n"

      "💡 **Exemple d'interaction attendue** :\n"
      "Utilisateur : \"Je cherche des articles sur l'intelligence artificielle.\"\n"
      "Assistant : \"Vous recherchez des articles sur l'intelligence artificielle. Voulez-vous préciser une période ou une source spécifique ?\"\n\n"

      "🚀 Adopte un ton amical et engageant. Fournis des réponses claires et adaptées au contexte."
    ).format(
        query=user_query, 
        data_model=self.graph, 
        context=self.context, 
    )
    interaction = self.model.generate(prompt)
    return interaction
