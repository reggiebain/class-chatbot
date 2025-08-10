# scripts/ingest_docs.py
"""Scan a folder of course documents (pdf, md, txt) and save raw text pieces to disk.
"""
import pathlib
from tqdm import tqdm
import sys
from typing import List

from langchain_community.document_loaders import UnstructuredPDFLoader, TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

DATA_DIR = "./data"
OUT_DIR = "./data/processed"


def load_and_split(path: str, chunk_size=1000, chunk_overlap=200):
    path = pathlib.Path(path)
    loader = None
    if path.suffix.lower() == ".pdf":
        loader = UnstructuredPDFLoader(str(path))
    else:
        loader = TextLoader(str(path), encoding="utf8")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs)


if __name__ == "__main__":
    src_dir = pathlib.Path(DATA_DIR)
    out_dir = pathlib.Path(OUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    files = list(src_dir.glob("**/*.*"))
    for f in tqdm(files):
        try:
            chunks = load_and_split(f)
            for i, c in enumerate(chunks):
                out_file = out_dir / f"{f.stem}_chunk_{i}.json"
                out_file.write_text(c.page_content)
        except Exception as e:
            print(f"failed {f}: {e}")
