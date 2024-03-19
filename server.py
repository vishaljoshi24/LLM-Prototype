"""
The Flask server for the LLM prototype.
"""

import os
import signal
from flask import Flask, request, jsonify
from flask_cors import cross_origin
import llama2local

app = Flask(__name__)

chain = llama2local.qa_bot()


@app.route("/ping")
@cross_origin()
def ping():
    """Checks whether the server is ready."""
    return "OK", 200


@app.route("/query", methods=["POST"])
@cross_origin()
def handle_query():
    """
    Handle a user query and return a response.
    """
    query = request.form["query"]

    response = llama2local.chatbot_response(query, chain)

    return jsonify(
        {
            "response": str(response["result"]),
            "sources": str(response["source_documents"]),
        }
    )


@app.get("/kill")
def handle_kill():
    """
    Kill the server process.
    """
    os.kill(os.getpid(), signal.SIGINT)

    return jsonify({"success": True, "message": "Killing server..."})


@app.errorhandler(500)
def handle_error(_error):
    """
    Handle errors.
    """
    return jsonify({"error": "Internal Server Error"}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
