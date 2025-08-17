import click
from langsmith import traceable
from ls_utils.langsmith_utils import init_langsmith
from app.utils import load_vectorstore, build_qa_chain
from app.moderation import ModerationService  # ✅ moderation step
from config import LLM_MODEL

# Initialize LangSmith
init_langsmith()
moderator = ModerationService()  # uses OPENAI_API_KEY from env


@traceable(name="moderation_step")
def run_moderation(question: str):
    """Run moderation check as its own LangSmith traceable step."""
    normalized, raw = moderator.check(question)
    return {"normalized": normalized, "raw": raw}


@traceable(name="rag_step")
def run_rag(vs, k, question):
    """RAG QA chain step, traceable in LangSmith."""
    chain = build_qa_chain(vectorstore=vs, k=k)
    return chain.invoke(question)


@traceable(name="moderated_rag_cli_question")
def ask_moderated_question(vs, k, question):
    """
    Full pipeline trace:
    - Step 1: moderation
    - Step 2: RAG QA (only if safe)
    Returns string for user, but trace logs full metadata.
    """
    # Step 1: moderation
    moderation_result = run_moderation(question)
    norm, raw = moderation_result["normalized"], moderation_result["raw"]

    if norm["flagged"]:
        # Moderation flagged: return string for user
        return f"⚠️ Input flagged. Categories: {norm['categories']}"

    # Step 2: RAG QA
    resp_dict = run_rag(vs, k, question)

    # Normalize chain output to a string
    if isinstance(resp_dict, dict):
        for key in ["result", "response", "output_text"]:
            if key in resp_dict:
                resp_text = resp_dict[key]
                break
        else:
            resp_text = next(iter(resp_dict.values()))
    else:
        resp_text = str(resp_dict)

    # LangSmith automatically logs the full return value of the trace,
    # so we can include moderation + raw data as metadata if needed
    return resp_text


@click.command()
@click.option("--k", default=4, help="Number of docs to retrieve")
def chat(k):
    vs = load_vectorstore()
    print("RAG chat CLI (moderated). Type 'exit' to quit.")
    while True:
        q = input("User: ")
        if q.strip().lower() in ("exit", "quit"):
            break

        resp_text = ask_moderated_question(vs, k, q)
        print("Assistant:", resp_text)


if __name__ == '__main__':
    chat()
