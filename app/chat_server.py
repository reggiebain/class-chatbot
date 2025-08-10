# app/chat_server.py
from fastapi import FastAPI
from pydantic import BaseModel
from app.utils import load_vectorstore, build_qa_chain
from langsmith.langsmith_utils import create_run_record, log_example

app = FastAPI()
vs = load_vectorstore()
chain = build_qa_chain(vectorstore=vs)

class Query(BaseModel):
    question: str

@app.post('/query')
async def query(q: Query):
    run = create_run_record('api-run')
    answer = chain.run(q.question)
    log_example(run, q.question, answer)
    return {"answer": answer}
