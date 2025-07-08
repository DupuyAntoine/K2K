from flask import Flask # type: ignore

app = Flask('Agent App')

from flask import Flask, request, jsonify # type: ignore
from eval.agents.interaction_agent import InteractionAgent
from eval.agents.response_agent import ResponseConstructionAgent
from eval.agents.file_extraction_agent import FileExtractionAgent
from eval.agents.no_agent import NoAgent
from eval.eval import run_tests, run_tests_noagent

app = Flask('Agent App')

no_agent = NoAgent(model="llama-3.3-70b-versatile")
interaction_agent = InteractionAgent(model="llama-3.3-70b-versatile")
extraction_agent = FileExtractionAgent(model="llama-3.3-70b-versatile")
response_agent = ResponseConstructionAgent(model="llama-3.3-70b-versatile")

@app.route('/eval', methods=['POST'])
def process_eval():
    data = request.get_json()
    data_model = data.get('graph', '')
    response = run_tests(data_model, interaction_agent, extraction_agent, response_agent)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
