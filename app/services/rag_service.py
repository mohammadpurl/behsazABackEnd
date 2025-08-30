# import os
# from typing import List, Dict, Any, Optional
# from langchain_openai.chat_models import ChatOpenAI
# from langchain.schema import Document
# from services.document_service import DocumentService
# from services.vector_store_service import VectorStoreService
# from models.rag_models import ProcessingStats, SearchResult
# from schemas.rag_schemas import QuestionResponse, VectorStoreStatus, DocumentInfo
# import time


# class RAGService:
#     def __init__(self, data_dir: str = "data", vectorstore_dir: str = "vectorstore"):
#         self.document_service = DocumentService(data_dir)
#         self.vector_store_service = VectorStoreService(vectorstore_dir)
#         self.llm = ChatOpenAI(model="gpt-3.5-turbo")
#         self.is_initialized = False
#         self.processing_stats: Optional[ProcessingStats] = None

#     def initialize_system(self, force_rebuild: bool = False) -> bool:
#         """Initialize the RAG system - load documents and create vector store"""
#         try:
#             # Try to load existing vector store first
#             if (
#                 not force_rebuild
#                 and self.vector_store_service.load_existing_vectorstore()
#             ):
#                 self.is_initialized = True
#                 print("Using existing vector store")
#                 return True

#             # Load and process documents
#             print("Loading documents...")
#             documents = self.document_service.load_pdfs()

#             if not documents:
#                 print("No documents found, trying fallback URLs...")
#                 fallback_urls = [
#                     "https://docs.python.org/3/tutorial/index.html",
#                     "https://realpython.com/python-basics/",
#                 ]
#                 documents = self.document_service.load_urls(fallback_urls)

#                 if not documents:
#                     raise ValueError("No documents could be loaded")

#             # Chunk documents
#             print("Chunking documents...")
#             chunks = self.document_service.chunk_documents(documents)

#             # Create vector store
#             if self.vector_store_service.initialize_vectorstore(chunks):
#                 self.is_initialized = True

#                 # Get processing stats
#                 self.processing_stats = self.document_service.get_processing_stats(
#                     documents, chunks
#                 )

#                 print(f"RAG system initialized successfully!")
#                 print(f"Documents: {self.processing_stats.total_documents}")
#                 print(f"Chunks: {self.processing_stats.total_chunks}")
#                 return True
#             else:
#                 return False

#         except Exception as e:
#             print(f"Error initializing RAG system: {e}")
#             return False

#     def ask_question(self, question: str, context_length: int = 3) -> QuestionResponse:
#         """Ask a question and get an answer using RAG"""
#         if not self.is_initialized:
#             raise ValueError(
#                 "RAG system not initialized. Call initialize_system() first."
#             )

#         try:
#             # Retrieve relevant documents
#             retriever = self.vector_store_service.get_retriever()
#             documents = retriever.invoke(question)

#             # Extract context and sources
#             context_text = "\n\n".join([doc.page_content for doc in documents])
#             sources = list(
#                 set([doc.metadata.get("source", "unknown") for doc in documents])
#             )

#             # Generate answer using LLM
#             prompt = f"""Context:\n{context_text}\n\nQuestion: {question}\n\nAnswer based on the context above:"""

#             response = self.llm.invoke(prompt)
#             answer = str(response.content)

#             return QuestionResponse(
#                 question=question,
#                 answer=answer,
#                 sources=sources,
#                 confidence=None,  # Could be calculated based on similarity scores
#             )

#         except Exception as e:
#             print(f"Error generating answer: {e}")
#             return QuestionResponse(
#                 question=question,
#                 answer=f"Sorry, I couldn't generate an answer due to an error: {str(e)}",
#                 sources=[],
#                 confidence=0.0,
#             )

#     def search_documents(self, query: str, k: int = 5) -> List[SearchResult]:
#         """Search for relevant documents"""
#         if not self.is_initialized:
#             raise ValueError("RAG system not initialized")

#         return self.vector_store_service.search_similar(query, k)

#     def get_system_status(self) -> VectorStoreStatus:
#         """Get current system status"""
#         if not self.is_initialized:
#             return VectorStoreStatus(
#                 is_initialized=False, document_count=0, total_chunks=0, documents=[]
#             )

#         try:
#             collection_info = self.vector_store_service.get_collection_info()

#             if "error" in collection_info:
#                 return VectorStoreStatus(
#                     is_initialized=False, document_count=0, total_chunks=0, documents=[]
#                 )

#             # Get document information
#             documents = self.document_service.get_document_info(
#                 []
#             )  # This needs to be fixed

#             return VectorStoreStatus(
#                 is_initialized=True,
#                 document_count=collection_info.get("total_documents", 0),
#                 total_chunks=collection_info.get("total_documents", 0),
#                 documents=[DocumentInfo(**doc) for doc in documents],
#             )

#         except Exception as e:
#             print(f"Error getting system status: {e}")
#             return VectorStoreStatus(
#                 is_initialized=False, document_count=0, total_chunks=0, documents=[]
#             )

#     def rebuild_vectorstore(self) -> bool:
#         """Force rebuild the vector store"""
#         print("Rebuilding vector store...")
#         return self.initialize_system(force_rebuild=True)

#     def get_processing_stats(self) -> Optional[ProcessingStats]:
#         """Get document processing statistics"""
#         return self.processing_stats
import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from app.services.document_service import load_and_split_documents
from app.config import settings

embeddings = OpenAIEmbeddings()

# ساخت یا بارگذاری VectorStore
if not os.path.exists(settings.VECTORSTORE_DIR):
    docs = load_and_split_documents()
    vectordb = Chroma.from_documents(
        docs, embeddings, persist_directory=settings.VECTORSTORE_DIR
    )
    vectordb.persist()
else:
    vectordb = Chroma(
        persist_directory=settings.VECTORSTORE_DIR, embedding_function=embeddings
    )

retriever = vectordb.as_retriever()

# ساخت QA chain
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever, chain_type="stuff")


def answer_question(question: str) -> str:
    return qa_chain.run(question)
