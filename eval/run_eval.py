# eval/run_eval.py
from ls_utils.langsmith_utils import init_langsmith, get_langsmith_client
from app.utils import load_vectorstore, build_qa_chain
from app.chat_server import ask_moderated_question, vs
from eval.custom_evaluators import correctness, retrieval_relevance
from eval.bulid_dataset import build_dataset
from langsmith.evaluation import evaluate
import pandas as pd

init_langsmith()
dataset = build_dataset()
client = get_langsmith_client()

# Needs to replicate the whole pipeline we do in chat_server
def rag_pipeline(inputs: dict) -> dict:
    question = inputs['question']
    k = inputs.get('k', 4)

    # Rebuild chain and stuff
    chain = build_qa_chain(vectorstore=vs, k=k)
    retrieved_docs = chain.retriever.invoke(question)
    answer = chain.run(question)

    #answer = ask_moderated_question(vs, k, question)
    return {"answer": answer, "documents": retrieved_docs}

if __name__ == "__main__":
    experiment_results = client.evaluate(
        rag_pipeline,
        data=dataset.name,
        evaluators=[correctness, retrieval_relevance],
        experiment_prefix="syllabus-eval",
        metadata={"version": "v1"},
    )
    #df = experiment_results.to_pandas()
