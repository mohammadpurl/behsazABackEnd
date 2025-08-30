import os
from typing import List
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from app.services.document_service import load_and_split_documents
from app.config import settings

# Initialize services only when needed (lazy loading)
_embeddings = None
_vectordb = None
_qa_chain = None


def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = OpenAIEmbeddings()
    return _embeddings


def get_vectordb():
    global _vectordb
    if _vectordb is None:
        embeddings = get_embeddings()
        if not os.path.exists(settings.VECTORSTORE_DIR):
            # Create vector store only when needed
            docs = load_and_split_documents()
            _vectordb = Chroma.from_documents(
                docs, embeddings, persist_directory=settings.VECTORSTORE_DIR
            )
            _vectordb.persist()
        else:
            _vectordb = Chroma(
                persist_directory=settings.VECTORSTORE_DIR,
                embedding_function=embeddings,
            )
    return _vectordb


def get_qa_chain():
    global _qa_chain
    if _qa_chain is None:
        vectordb = get_vectordb()
        retriever = vectordb.as_retriever()
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        _qa_chain = RetrievalQA.from_chain_type(
            llm, retriever=retriever, chain_type="stuff"
        )
    return _qa_chain


def answer_question(question: str) -> str:
    """Lightweight question answering function"""
    try:
        qa_chain = get_qa_chain()
        return qa_chain.invoke({"query": question})["result"]
    except Exception as e:
        return f"Error: {str(e)}"
