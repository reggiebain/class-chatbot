# langsmith/langsmith_utils.py
from langsmith import Client
import os

from config import LANGSMITH_API_KEY, LANGSMITH_PROJECT

_client = None

def get_langsmith_client():
    global _client
    if _client is None:
        _client = Client(api_key=LANGSMITH_API_KEY)
    return _client

def init_langsmith():
    os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
    os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT
    os.environ["LANGCHAIN_TRACING_V2"] = "true"

def load_prompt_from_langsmith(prompt_name: str):
    """Fetch a stored prompt from LangSmith by name."""
    client = get_langsmith_client()
    #prompt = client.read_prompt(prompt_name)
    prompt = client.pull_prompt("syllabus-bot-prompt", include_model=True)
    from langchain.prompts import ChatPromptTemplate
    return ChatPromptTemplate.from_messages(prompt.messages)
