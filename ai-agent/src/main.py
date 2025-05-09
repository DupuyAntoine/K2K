from flask import Flask, request, jsonify # type: ignore
from agents.interaction_agent import InteractionAgent
from agents.response_agent import ResponseConstructionAgent
from agents.file_extraction_agent import FileExtractionAgent
from agents.evaluation.eval import run_tests

app = Flask('Agent App')

interaction_agent = InteractionAgent(model="llama-3.3-70b-versatile")
extraction_agent = FileExtractionAgent(model="llama-3.3-70b-versatile")
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
    files = extraction_agent.extract_files(interaction, data_model)
    return jsonify(files)

@app.route('/response', methods=['POST'])
def process_response():
    data = request.get_json()
    interaction = data.get('request', '')
    files = data.get('files', '')
    
    response = response_agent.construct_response(interaction, files)

    return jsonify({ 'text': response })

@app.route('/eval', methods=['POST'])
def process_eval():
    data = request.get_json()
    # data_model = data.get('graph', '')
    response = run_tests(None, interaction_agent, extraction_agent, response_agent)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
