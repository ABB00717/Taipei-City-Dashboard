# app.py
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from config import load_environment
from database import get_db
from ai_model import setup_ai_model, setup_check_chain
from chat_history import getSessionConversation

def create_app():
    app = Flask(__name__, static_folder=".")
    CORS(app)
    return app

# New function to get session history without modifying it
def get_read_only_session_history(session_id: str):
    return getSessionConversation(session_id)

# Route handlers
def index():
    return send_from_directory(".", "index.html")

def serve_js():
    return send_from_directory(".", "app.js")

def generate_response():
    data = request.json
    prompt = data.get("prompt")
    session_id = data.get("session_id", "default")

    try:
        # Use the read-only session history
        session_history = get_read_only_session_history(session_id)
        
        sql_response = main_chain.invoke({
            "question": prompt,
            "history": session_history
        })
        
        promising_response = chain_check.invoke({
            "question": prompt,
            "sql_response": sql_response,
            "history": session_history
        })
        
        # Manually update the session history after processing
        session_history.add_user_message(prompt)
        session_history.add_ai_message(promising_response)
        
        return jsonify({"response": promising_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Main application setup
load_environment()
app = create_app()
db = get_db()
main_chain = setup_ai_model(db)
chain_check = setup_check_chain()

# Remove RunnableWithMessageHistory wrappers
# chain_with_history and check_with_history are no longer used

# Route definitions
app.route("/")(index)
app.route("/app.js")(serve_js)
app.route("/generate", methods=["POST"])(generate_response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)