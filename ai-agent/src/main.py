from flask import Flask, request, jsonify # type: ignore
from agents.interaction_agent import InteractionAgent
from agents.response_agent import ResponseAgent

# "llama-3.3-70b-versatile"

app = Flask('Agent App')

interaction_agent = InteractionAgent(model="llama-3.3-70b-versatile")
response_agent = ResponseAgent(model="llama-3.3-70b-versatile")

@app.route('/interact', methods=['POST'])
def process_interact():
    data = request.get_json()
    req = data.get('request', '')
    
    # Traitement simulé avec Llama 3.3
    response_text = interaction_agent.process_query(req)

    return jsonify({ 'text': response_text })

@app.route('/response', methods=['POST'])
def process_response():
    data = request.get_json()
    req = data.get('request', '')
    
    # Traitement simulé avec Llama 3.3
    response_text = response_agent.construct_response(req)

    return jsonify({ 'text': response_text })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
