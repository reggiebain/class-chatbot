# Syllabus RAG Chatbot

This project is a **Retrieval-Augmented Generation (RAG) chatbot** for answering questions about a syllabus.  

It consists of:
- A **FastAPI backend** (`app/`) that runs the RAG pipeline (vectorstore + LLM + moderation).
- A **Streamlit frontend** (`streamlit_app/`) that provides a simple chat UI.
- Implementation of **LangSmith** tracing and evaluation (`eval/`) with dashboard monitoring of live queries via streamlit app.
- A `Makefile` with convenient commands to run the system.

#### Screenshots
- [See a sample conversation here.](./img/queries_sample.png)
- [Table of LangSmith Evaluation Traces using LLM-as-judge](./img/syllabus_eval_table.png)
- [A detailed LangSmith trace of a query](./img/langsmith_successful_query.png)
- [A query that gets flagged by moderator](./img/safety_example.png)
---

## Getting Startedg

### 1. Clone the repo
```bash
git clone https://github.com/reggiebain/class-chatbot/tree/main
cd class-chatbot
```

### 2. Create & activate a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
make install
```

Notable dependencies include:
- `fastapi`
- `uvicorn`
- `langchain`
- `streamlit`
- `requests`
- `langsmith`

---

## Running the App

We use a `Makefile` to simplify commands.

### Run only the backend (FastAPI)
```bash
make server
```
Starts the API at: [http://localhost:8000](http://localhost:8000)

### Run only the frontend (Streamlit)
```bash
make frontend
```
Starts the UI at: [http://localhost:8501](http://localhost:8501)

### Run both (backend + frontend)
```bash
make dev
```
---

## Example Usage

Ask your syllabus bot things like:
- “When are assignments due?”
- “What chapters should I read before midterm?”
- “What is the late work policy?”

```
User: What’s the grading breakdown?
Bot: The grading breakdown is 40% exams, 30% projects, 20% homework, and 10% participation.
```

---

## Future Improvements
- Dockerize frontend + backend
- Deploy to cloud (e.g., Render, Fly.io, AWS)
