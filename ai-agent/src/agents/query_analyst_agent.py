from agents.model.model import Model

class QueryAnalystAgent:
  def __init__(self, model):
    self.model = Model(model_name=model)
    self.context = None
    self.ontology = None
    self.history = None

  def process_query(self, user_query, context, history, ontology):
    self.ontology = ontology
    self.context = context
    self.history = history
    prompt = (
      "**Assistant de recherche intelligent**\n\n"
      "Tu es un assistant spécialisé dans la recherche de données. "
      "Ton objectif est d’aider l'utilisateur à affiner sa requête en fonction du modèle de données disponible. "
      "Tu dois le guider avec des questions pertinentes si sa requête est incomplète ou lui récapituler ses critères pour validation.\n\n"
      
      "**Analyse de la requête** :\n"
      "Requête utilisateur : '{query}'\n"
      "Modèle de données (ontologie de représentation des jeux de données) : {ontology}\n"
      "Données contextuelles au domaine, pour t'aider à déterminer les critères de la requête utilisateur : {context}\n"
      "Historique du dialogue avec l'utilisateur : {history}\n"

      "**Processus d’assistance** :\n"
      "1️ **Déterminer les informations fournies** : Quels critères sont déjà mentionnés ?\n"
      "2️ **Identifier les critères manquants** en comparant la requête au modèle de données.\n"
      "3️ **Si la requête est incomplète**, poser des questions ciblées pour clarifier les attentes de l'utilisateur.\n"
      "4️ **Si la requête est complète**, récapituler les critères extraits et demander confirmation.\n\n"

      "**Exemple d'interaction attendue** :\n"
      "Utilisateur : \"Je cherche des articles sur l'intelligence artificielle.\"\n"
      "Assistant : \"Vous recherchez des articles sur l'intelligence artificielle. Voulez-vous préciser une période ou une source spécifique ?\"\n\n"

      "Adopte un ton amical et engageant. Fournis des réponses claires et adaptées au contexte."
    ).format(
        query=user_query, 
        ontology=self.ontology, 
        context=self.context,
        history=self.history
    )
    analysis = self.model.generate(prompt)
    return analysis
