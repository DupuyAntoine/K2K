from flask import Flask, request, jsonify # type: ignore
from agents.query_analyst_agent import QueryAnalystAgent
from agents.data_identification_agent import DataIdentificationAgent
from agents.response_agent import ResponseConstructionAgent

app = Flask('AgentApp')

# Initialisation des agents
query_analyst_agent = QueryAnalystAgent(model="llama-3.3-70b-versatile")
data_identification_agent = DataIdentificationAgent(model="llama-3.3-70b-versatile")
response_agent = ResponseConstructionAgent(model="llama-3.3-70b-versatile")

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

        # 1. Analyse de la requête (message + contexte + historique + ontologie)
        analysis = query_analyst_agent.process_query(
            user_query=user_message,
            context=context,
            history=history,
            ontology=ontology
        )

        # 2. Extraction des fichiers à partir de l’interaction + contexte
        # files = data_identification_agent.extract_files(
        #     analysis=analysis,
        #     context_data=context,
        #     ontology=ontology
        # )

        files = []

        # 3. Construction de la réponse finale
        response_text = response_agent.construct_response(
            analysis=analysis,
            files=files,
            ontology=ontology
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
