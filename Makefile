# ========== Project Configuration ==========
# Load environment variables from .env (if present)
-include .env
export $(shell sed 's/=.*//' .env 2>/dev/null)

# Directories
DATA_DIR := ./data
PROCESSED_DIR := ./data/processed
VECTORSTORE_DIR := $(VECTORSTORE_DIR)
VENV_DIR := .venv-rag-langsmith

# Python executables inside venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip

.PHONY: all install reinstall ingest embed build chat server clean

# ========== Main Targets ==========

# Full pipeline: ingest -> embed -> build
all: ingest embed build

install:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "📦 Creating virtual environment: $(VENV_DIR)"; \
		python3 -m venv $(VENV_DIR); \
	else \
		echo "✅ Virtual environment already exists: $(VENV_DIR)"; \
	fi
	@echo "🔧 Installing/updating dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install unstructured[all-docs] unstructured_pytesseract && \
	brew install --quiet poppler tesseract
	@echo "✅ Activate with: source $(VENV_DIR)/bin/activate"

reinstall:
	@echo "♻️  Rebuilding virtual environment from scratch..."
	rm -rf $(VENV_DIR)
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "✅ Fresh venv ready. Activate with: source $(VENV_DIR)/bin/activate"

ingest:
	@echo "📄 Ingesting raw documents from $(DATA_DIR)..."
	#$(PYTHON) scripts/ingest_docs.py
	$(PYTHON) -m scripts.ingest_docs
embed:
	@echo "🔢 Creating embeddings..."
	#$(PYTHON) scripts/embed_docs.py
	$(PYTHON) -m scripts.embed_docs
build:
	@echo "📦 Building vectorstore..."
	#$(PYTHON) scripts/build_vectorstore.py
	$(PYTHON) -m scripts.build_vectorstore
chat:
	@echo "💬 Starting CLI chatbot..."
	$(PYTHON) -m app.chat_cli

server:
	@echo "🚀 Starting FastAPI server..."
	$(PYTHON) -m uvicorn app.chat_server:app --reload

frontend:
	@echo "🖥️ Starting Streamlit app..."
	streamlit run streamlit_app/streamlit_app.py --server.port 8501

clean:
	@echo "🧹 Cleaning processed data and vectorstore..."
	rm -rf $(PROCESSED_DIR) $(VECTORSTORE_DIR)
	mkdir -p $(PROCESSED_DIR) $(VECTORSTORE_DIR)
