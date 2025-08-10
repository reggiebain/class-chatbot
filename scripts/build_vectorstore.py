# scripts/build_vectorstore.py
from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.schema import Document
from pathlib import Path
import json
import numpy as np
from config import VECTORSTORE_DIR, EMBEDDING_MODEL

EMB = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)

OUT = Path(VECTORSTORE_DIR)
embs = np.load(OUT / "embeddings.npy")
meta = json.loads((OUT / "meta.json").read_text())

docs = [Document(page_content=open(m["source"]).read(), metadata=m) for m in meta]
faiss = FAISS.from_documents(docs, EMB)
faiss.save_local(str(OUT))
