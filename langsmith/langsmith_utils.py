# langsmith/langsmith_utils.py
from langsmith import Client
from config import LANGSMITH_API_KEY, LANGSMITH_PROJECT

client = Client(api_key=LANGSMITH_API_KEY)


def create_run_record(name: str, metadata: dict = None):
    run = client.create_run(name=name, project=LANGSMITH_PROJECT, metadata=metadata or {})
    return run


def log_example(run, input_text: str, output_text: str, score: float = None):
    client.log_example(run_id=run.id, input=input_text, output=output_text, score=score)


# Add more helpers for logging chain events, embeddings, evaluation artifacts, etc.
