from flask import Flask, request, jsonify # type: ignore

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    req = data.get('request', '')
    
    # Traitement simulé avec Llama 3.3
    response_text = f"Réponse simulée pour la question: '{req}' (traitée par Llama 3.3)"
    
    return jsonify({ 'response': response_text })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
