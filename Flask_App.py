from flask import Flask, request, jsonify
from flask_cors import CORS
import llama2local
from utils import evaluation

#################
# Flask Section #
#################
flask_app = Flask(__name__)
CORS(flask_app)
chain = llama2local.qa_bot()


@flask_app.route('/', methods=["POST"])
def process_prompt():
    input_json = request.get_json(force=True)
    prompt = input_json.get("prompt")
    # Returns error if prompt is missing
    if not prompt:
        return jsonify({'error': 'Prompt is missing'}), 400

    chatbot_response = llama2local.chatbot_response(prompt, chain)
    return jsonify({'Chatbot': str(chatbot_response["result"]), "Sources": str(chatbot_response["source_documents"])})


@flask_app.route('/evaluate', methods=["POST"])
def evaluate():
    input_json = request.get_json(force=True)
    evaluation.submit_rating(input_json.get("chatlog"), input_json.get("theme"), input_json.get("coherency"),
                             input_json.get("fluency"), input_json.get("model"), input_json.get("temperature"),
                             input_json.get("top_p"), input_json.get("top_k"), input_json.get("repetition"),
                             input_json.get("max_length"))
    return jsonify({'Result': "evaluation saved"})


# Generic error handling
@flask_app.errorhandler(500)
def handle_500(error):
    return jsonify({'error': 'Internal server error'}), 500


# Server shutdown
@flask_app.get('/shutdown')
def shutdown():
    flask_app.terminate()
    return 'Server shutting down...'


if __name__ == "__main__":
    flask_app.run(port=5000, debug=False)
