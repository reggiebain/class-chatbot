# 📘 Syllabus RAG Chatbot

This project is a **Retrieval-Augmented Generation (RAG) chatbot** for answering questions about a syllabus.  

It consists of:
- A **FastAPI backend** (`app/`) that runs the RAG pipeline (vectorstore + LLM + moderation).
- A **Streamlit frontend** (`streamlit_app/`) that provides a simple chat UI.
- A `Makefile` with convenient commands to run the system.

---

## 🚀 Getting Started

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

## 🖥️ Running the App

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
Runs the backend in the background and starts the frontend in the foreground.

---

## 📂 Project Structure
```
your_project/
├── app/                     # Backend (FastAPI)
│   ├── chat_server.py       # RAG + moderation API
│   ├── utils.py             # Vectorstore + chain helpers
│   ├── moderation.py        # Moderation service
│   └── ...
├── streamlit_app/           # Frontend (Streamlit)
│   └── streamlit_app.py     # Chat UI
├── requirements.txt         # Python dependencies
├── Makefile                 # Run commands
└── README.md                # Project docs
```

---

## ⚠️ Notes

- The `dev` command runs the FastAPI server in the background.  
  If you stop Streamlit with `Ctrl+C`, the backend may still be running.  
  To kill it:
  ```bash
  lsof -i:8000   # Find process ID
  kill <PID>     # Stop it
  ```
- Adjust `API_URL` in `streamlit_app/streamlit_app.py` if deploying somewhere other than `localhost:8000`.

---

## ✨ Example Usage

Ask your syllabus bot things like:
- “When are assignments due?”
- “What chapters should I read before midterm?”
- “What is the late work policy?”

```
User: What’s the grading breakdown?
Bot: The grading breakdown is 40% exams, 30% projects, 20% homework, and 10% participation.
```

---

## 🔮 Future Improvements
- Dockerize frontend + backend
- Deploy to cloud (e.g., Render, Fly.io, AWS)
- Add LangSmith eval traces in the frontend
