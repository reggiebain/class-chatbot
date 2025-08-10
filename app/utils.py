# app/utils.py
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from config import VECTORSTORE_DIR, LLM_MODEL


def load_vectorstore(path: str = VECTORSTORE_DIR):
    vs = FAISS.load_local(path)
    return vs


def build_qa_chain(llm=None, vectorstore=None, k=4):
    llm = llm or ChatOpenAI(model_name=LLM_MODEL)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k})
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    return chain
