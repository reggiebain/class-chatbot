# scripts/embed_docs.py
from pathlib import Path
from sentence_transformers import SentenceTransformer
import json

from config import EMBEDDING_MODEL, VECTORSTORE_DIR

EMBED_MODEL = SentenceTransformer(EMBEDDING_MODEL)

RAW_DIR = Path("./data/processed")
OUT_DIR = Path(VECTORSTORE_DIR)
OUT_DIR.mkdir(parents=True, exist_ok=True)

embeddings = []
meta = []
for file in RAW_DIR.glob("*.json"):
    text = file.read_text()
    vec = EMBED_MODEL.encode(text)
    embeddings.append(vec.tolist())
    meta.append({"source": str(file)})

# save as a simple numpy/pickle or integrate with FAISS in build_vectorstore.py
import numpy as np
np.save(OUT_DIR / "embeddings.npy", np.array(embeddings))
import json
(OUT_DIR / "meta.json").write_text(json.dumps(meta))
