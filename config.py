# config.py
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
VECTORSTORE_DIR = os.getenv("VECTORSTORE_DIR", "./vectorstore")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# LLM config
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH")

# LangSmith project context
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "rag-course-chat")
