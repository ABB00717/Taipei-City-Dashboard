import os
from dotenv import load_dotenv

def load_environment():
    load_dotenv()
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = get_env_or_default("LANGCHAIN_API_KEY", "")
    os.environ["OPENAI_API_KEY"] = get_env_or_default("OPENAI_API_KEY", "")
    os.environ["TAVILY_API_KEY"] = get_env_or_default("TAVILY_API_KEY", "")

def get_env_or_default(key, default):
    value = os.getenv(key)
    if value is None or value.strip() == '':
        print(f"Warning: Environment variable {key} is not set. Using default value: {default}")
        return default
    return value