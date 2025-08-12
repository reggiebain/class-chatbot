# scripts/build_vectorstore.py
from langchain_community.vectorstores import FAISS
#from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from pathlib import Path
import json
import numpy as np
import os

from config import VECTORSTORE_DIR, EMBEDDING_MODEL

# Make sure the API key is available
if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

#EMB = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

out_dir = Path(VECTORSTORE_DIR)
meta_file = out_dir / "meta.json"
if not meta_file.exists():
    raise FileNotFoundError(f"Metadata file not found: {meta_file}")

meta = json.loads(meta_file.read_text())
docs = [
    Document(page_content=open(m["source"]).read(), metadata=m)
    for m in meta
]

# Build FAISS index with OpenAI embeddings
vectorstore = FAISS.from_documents(docs, embeddings)
vectorstore.save_local(str(out_dir))

print(f"✅ Vectorstore built and saved to {out_dir}")        

#embs = np.load(OUT / "embeddings.npy")
#meta = json.loads((OUT / "meta.json").read_text())

#docs = [Document(page_content=open(m["source"]).read(), metadata=m) for m in meta]
#faiss = FAISS.from_documents(docs, EMB)
#faiss.save_local(str(OUT))
