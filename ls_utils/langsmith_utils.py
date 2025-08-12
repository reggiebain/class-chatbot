# langsmith/langsmith_utils.py
from langsmith import Client
import os

from config import LANGSMITH_API_KEY, LANGSMITH_PROJECT

def get_langsmith_client():
    client = Client(api_key=LANGSMITH_API_KEY)

def init_langsmith():
    os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
    os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT
    os.environ["LANGCHAIN_TRACING_V2"] = "true"


#def create_run_record(name: str, inputs: dict = None, run_type: str = "chain", metadata: dict = None):
#    inputs = inputs or {}
#    run = client.create_run(
#            name=name,
#            inputs=inputs,
#            run_type = run_type,
#            project=LANGSMITH_PROJECT, 
#            metadata=metadata or {})
#    return run


#def log_example(run, input_text: str, output_text: str, score: float = None):
    # Attach inputs/outputs to the run metadata (or custom data)
    # This depends on how your run object supports it, assuming 'inputs' and 'outputs' fields:
#    run.inputs = {"text": input_text}
#    run.outputs = {"text": output_text}
    # If score needs to be attached as metadata:
#    if score is not None:
#        run.metadata["score"] = score

    # Now create an example from the updated run
#    example = client.create_example_from_run(
#        run=run,
#        dataset_name=LANGSMITH_PROJECT,  # or None if you don't use datasets
#        created_at=datetime.utcnow()
#    )
#    return example
    #client.create_example_from_run(
    #        run,
    #        {"text": input_text},
    #        {"text": output_text},
    #        score
    #        )
    #client.log_example(
    #        run_id=run.id, 
    #        input=input_text, 
    #        output=output_text, 
    #        score=score
    #        )


# Add more helpers for logging chain events, embeddings, evaluation artifacts, etc.
