# app/chat_cli.py
import click
from langsmith import traceable
from ls_utils.langsmith_utils import init_langsmith
from app.utils import load_vectorstore, build_qa_chain

from config import LLM_MODEL

init_langsmith()

@traceable(name="rag_cli_question")
def ask_question(vs, k, question):
    chain = build_qa_chain(vectorstore=vs,k=k)
    return chain.run(question)

@click.command()
@click.option("--k", default=4, help="Number of docs to retrieve")
def chat(k):
    #run = create_run_record("cli-run")
    vs = load_vectorstore()
    #chain = build_qa_chain(vectorstore=vs, k=k)
    print("RAG chat CLI. Type 'exit' to quit.")
    while True:
        q = input("User: ")
        if q.strip().lower() in ("exit", "quit"):
            break
        #resp = chain.run(q)
        resp = ask_question(vs, k, q)
        print("Assistant:", resp)
        #log_example(run, q, resp)


if __name__ == '__main__':
    chat()  
