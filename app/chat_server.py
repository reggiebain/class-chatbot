# app/chat_server.py
from fastapi import FastAPI
from pydantic import BaseModel
from app.utils import load_vectorstore, build_qa_chain
from app.moderation import ModerationService
from ls_utils.langsmith_utils import init_langsmith
from langsmith import traceable

init_langsmith()
moderator = ModerationService()

app = FastAPI()
vs = load_vectorstore()

class Query(BaseModel):
    question: str
    k: int=4

def extract_text_from_chain_output(output):
    if isinstance(output, str):
        return output
    if isinstance(output, dict):
        for key in ["result", "response", "output_text", "text", "answer"]:
            if key in output:
                return output[key]
        # fallback: first value in dict
        return str(next(iter(output.values())))
    return str(output)

@traceable(name='moderation_step')
def run_moderation(question: str):
    normalized, raw = moderator.check(question)
    return {"normalized": normalized, "raw": raw}

@traceable(name='rag_step')
def run_rag(vs, k, question):
    chain = build_qa_chain(vectorstore=vs, k=k)
    return chain.invoke(question)

def ask_moderated_question(vs, k, question):
    # Do moderation
    moderation_result = run_moderation(question)
    norm, raw = moderation_result["normalized"], moderation_result["raw"]

    if norm["flagged"]:
        # Moderation flagged: return string for user
        return f"⚠️ Input flagged. Categories: {norm['categories']}"
    # Do rag
    resp_dict = run_rag(vs, k, question)
    resp_text = extract_text_from_chain_output(resp_dict)
    return resp_text

@app.post('/query')
async def query(q: Query):
    answer = ask_moderated_question(vs, q.k, q.question)
    print(answer)
    return {"answer": answer}
