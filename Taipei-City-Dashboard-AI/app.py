import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableLambda

load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

app = Flask(__name__, static_folder=".")
CORS(app)

model = ChatOpenAI(model="gpt-3.5-turbo")

documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Goldfish are popular pets for beginners, requiring relatively simple care.",
        metadata={"source": "fish-pets-doc"},
    ),
    Document(
        page_content="Parrots are intelligent birds capable of mimicking human speech.",
        metadata={"source": "bird-pets-doc"},
    ),
    Document(
        page_content="Rabbits are social animals that need plenty of space to hop around.",
        metadata={"source": "mammal-pets-doc"},
    ),
]

message = """
Answer this question using the provided context only.

{question}

Context:
{context}
"""

vectorstore = Chroma.from_documents(
    documents,
    embedding=OpenAIEmbeddings(),
)

retriever = RunnableLambda(vectorstore.similarity_search).bind(k=1)  # select top result
retriever.batch(["cat", "shark", "human speech"])

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/app.js")
def serve_js():
    return send_from_directory(".", "app.js")

@app.route("/generate", methods=["POST"])
def generate_response():
    data = request.json
    prompt = data.get("prompt")

    try:
        promptAdjust = ChatPromptTemplate.from_messages([("human", message)])
        rag_chain = {"context": retriever, "question": RunnablePassthrough()} | promptAdjust | model
        response = rag_chain.invoke(prompt)
        
        return jsonify({"response": response.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)