import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent

# Load environment variables
def load_environment():
    load_dotenv()
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = get_env_or_default("LANGCHAIN_API_KEY", "")
    os.environ["OPENAI_API_KEY"] = get_env_or_default("OPENAI_API_KEY", "")
    os.environ["TAVILY_API_KEY"] = get_env_or_default("TAVILY_API_KEY", "")

# Function to safely get environment variables with default values
def get_env_or_default(key, default):
    value = os.getenv(key)
    if value is None or value.strip() == '':
        print(f"Warning: Environment variable {key} is not set. Using default value: {default}")
        return default
    return value

# Initialize Flask app
def create_app():
    app = Flask(__name__, static_folder=".")
    CORS(app)
    return app

# Setup AI model and tools
def setup_ai():
    model = ChatOpenAI(model="gpt-3.5-turbo")
    search = TavilySearchResults(max_results=2)
    tools = [search]
    return create_react_agent(model, tools)

# Route handlers
def index():
    return send_from_directory(".", "index.html")

def serve_js():
    return send_from_directory(".", "app.js")

def generate_response():
    data = request.json
    prompt = data.get("prompt")

    try:
        response = agent_executor.invoke({"messages": [HumanMessage(content=prompt)]})
        return jsonify({"response": response["messages"][-1].content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Main application setup
load_environment()
app = create_app()
agent_executor = setup_ai()

# Route definitions
app.route("/")(index)
app.route("/app.js")(serve_js)
app.route("/generate", methods=["POST"])(generate_response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)