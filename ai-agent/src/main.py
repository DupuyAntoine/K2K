from flask import Flask, request, jsonify # type: ignore
from agents.interaction_agent import InteractionAgent
from agents.response_agent import ResponseConstructionAgent
from agents.file_extraction_agent import FileExtractionAgent  # Import de l'agent d'extraction de fichiers

# "llama-3.3-70b-versatile"

app = Flask('Agent App')

interaction_agent = InteractionAgent(model="llama-3.3-70b-versatile")
response_agent = ResponseConstructionAgent(model="llama-3.3-70b-versatile")

@app.route('/interact', methods=['POST'])
def process_interact():
    data = request.get_json()
    req = data.get('request', '')
    data_model = data.get('graph', '')
    interaction = interaction_agent.process_query(req, data_model)
    return jsonify(interaction)

@app.route('/extract', methods=['POST'])
def process_extract():
    data = request.get_json()
    interaction = data.get('interaction', '')
    data_model = data.get('graph', '')
    files = interaction_agent.process_query(interaction, data_model)
    return jsonify(files)

@app.route('/response', methods=['POST'])
def process_response():
    data = request.get_json()
    interaction = data.get('request', '')
    files = data.get('files', '')
    
    response = response_agent.construct_response(interaction, files)

    return jsonify({ 'text': response })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
