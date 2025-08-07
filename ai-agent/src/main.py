import logging
from flask import Flask, request, jsonify # type: ignore
from agents.user_intent_agent import UserIntentAgent
from agents.query_analyst_agent import QueryAnalystAgent
from agents.data_identification_agent import DataIdentificationAgent
from agents.response_agent import ResponseConstructionAgent
from agents.model.model import Model

app = Flask('AgentApp')

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Initialisation des agents
user_intent_agent = UserIntentAgent(model="llama-3.3-70b-versatile")
query_analyst_agent = QueryAnalystAgent(model="llama-3.3-70b-versatile")
data_identification_agent = DataIdentificationAgent()
response_agent = ResponseConstructionAgent(model="llama-3.3-70b-versatile")
model = Model(model_name="llama-3.3-70b-versatile")

# TODO: user query's language recognition is buggy, probably because
# the overall prompt is in english, it leads to random frenglish responses
# or english only or french only responses // IMPORTANT
@app.route('/chat', methods=['POST'])
def chat():
  try:
    data = request.get_json()

    user_message = data.get('message', '')
    context = data.get('context', {})
    history = data.get('history', [])
    ontology = data.get('ontology', {})

    if not user_message:
      return jsonify({ "error": "Missing user message." }), 400

    # 0. Analyse de l'intention utilisateur (message + historique)
    intent_result = user_intent_agent.detect_intent(
      user_message=user_message
    )
    intent = intent_result.get("intent", "chitchat")
    lang = intent_result.get("lang", "en")

    # TODO: move this lines to a specialized chitchat agent // MODERATE
    if intent in ("gratitude", "chitchat", "general_question"):
      system_prompt = (
        f"You are a multilingual assistant. Always respond in the same language the user uses "
        f"following the user intent: {intent}. Keep it frendly and very short.\n"
        f"Here are some examples:\n"
        f"User: Bonjour, je cherche des données climatiques pour la France.\n"
        f"Assistant: Bien sûr ! Voici quelques jeux de données utiles pour la France.\n"
        f"User: Hola, ¿puedes ayudarme con datos de temperatura?\n"
        f"Assistant: Claro, aquí tienes algunos conjuntos de datos sobre la temperatura.\n\n"
        f"Now, respond to the user below in their language:\n\n"
        f"User: {user_message}\n"
        "Assistant:"
      )
      llm_response = model.generate(system_prompt)
      return jsonify({
        "response": llm_response.strip(),
        "files": [],
        "logs": {
          "analysis": None,
          "files": []
        }
      })

    # 1. Analyse de la requête (message + contexte + historique + ontologie)
    analysis = query_analyst_agent.process_query(
      user_query=user_message,
      intent=intent,
      context=context,
      history=history,
      ontology=ontology
    )

    files = []
    if intent in ("data_search"):
      # 2. Extraction des fichiers à partir de l’interaction + contexte
      files = data_identification_agent.identify_datasets(
        analysis=analysis
      )

    # 3. Construction de la réponse finale
    response_text = response_agent.construct_response(
      user_message=user_message,
      intent=intent,
      analysis=analysis,
      files=files,
      lang=lang
    )

    return jsonify({
      "response": response_text,
      "files": files,
      "logs": {
        "analysis": analysis,
        "files": files
      }
    })

  except Exception as e:
    return jsonify({ "error": str(e) }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
