# app/utils.py
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from ls_utils.langsmith_utils import load_prompt_from_langsmith


from config import VECTORSTORE_DIR, LLM_MODEL, OPENAI_API_KEY

def load_vectorstore(path: str = VECTORSTORE_DIR):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",  # must match ingestion
        api_key=OPENAI_API_KEY
    )
    vs = FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
    return vs


def build_qa_chain(llm=None, vectorstore=None, k=4, role=None, custom_prompt=None):
    llm = llm or ChatOpenAI(model_name=LLM_MODEL)
    retriever = vectorstore.as_retriever(
            search_type="similarity", 
            search_kwargs={"k": k}
    )
    chain = RetrievalQA.from_chain_type(
            llm=llm, 
            chain_type="stuff", 
            retriever=retriever,
            chain_type_kwargs={'prompt': custom_prompt},
    )
    return chain
