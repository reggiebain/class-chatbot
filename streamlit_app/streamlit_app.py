# streamlit_app/streamlit_app.py
import streamlit as st
import requests
# Add tracing to front end
from ls_utils.langsmith_utils import init_langsmith, get_langsmith_client
from langsmith import traceable

# Initialize LangSmith
init_langsmith()
client = get_langsmith_client()

# Backend URL
API_URL = "http://localhost:8000/query"  # Update if deployed elsewhere

st.set_page_config(page_title="Syllabus Chatbot", page_icon="📘", layout="wide")

st.title("SyllabusBot")
st.text("This LLM-driven app uses a RAG backend to answer queries about Physics 1. It also implements safety protocols to help protect users from harmful output.")
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for settings
#st.sidebar.header("Settings")
#k_value = st.sidebar.slider("Top-K documents to retrieve", 1, 10, 4)
k_value = 4


# Add traceable wrapper for frontend call
@traceable(name="frontend_chat_request")
def get_answer_from_backend(question: str, k: int = 4) -> dict:
    response = requests.post(API_URL, json={"question": question, "k": k})
    response.raise_for_status()
    return response.json()

# Chat UI
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me about the syllabus..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call FastAPI backend
    try:
        #response = requests.post(API_URL, json={"question": prompt, "k": k_value})
        #response.raise_for_status()
        #answer = response.json().get("answer", "⚠️ No answer returned.")
        response_data = get_answer_from_backend(prompt, k_value)
        answer = response_data.get("answer", "⚠️ No answer returned.")
    except Exception as e:
        answer = f"❌ Error contacting backend: {e}"

    # Add assistant message to chat
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
