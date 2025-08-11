# langsmith/langsmith_utils.py
from langsmith import Client
from config import LANGSMITH_API_KEY, LANGSMITH_PROJECT

client = Client(api_key=LANGSMITH_API_KEY)

def create_run_record(name: str, inputs: dict = None, run_type: str = "chain", metadata: dict = None):
    inputs = inputs or {}
    run = client.create_run(
            name=name,
            inputs=inputs,
            run_type = run_type,
            project=LANGSMITH_PROJECT, 
            metadata=metadata or {})
    return run


def log_example(run, input_text: str, output_text: str, score: float = None):
    client.create_example_from_run(
            run=run,
            inputs={"text": input_text},
            outputs={"text": output_text},
            score=score
            )
    #client.log_example(run_id=run.id, input=input_text, output=output_text, score=score)


# Add more helpers for logging chain events, embeddings, evaluation artifacts, etc.
