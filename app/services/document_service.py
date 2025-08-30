# import os
# from typing import List, Dict, Any
# from langchain_community.document_loaders import PyPDFLoader, UnstructuredURLLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.schema import Document
# from models.rag_models import DocumentChunk, ProcessingStats
# from datetime import datetime
# import time


# class DocumentService:
#     def __init__(self, data_dir: str = "data"):
#         self.data_dir = data_dir
#         self.text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1500, chunk_overlap=150
#         )

#     def load_pdfs(self) -> List[Document]:
#         """Load all PDF documents from the data directory"""
#         if not os.path.exists(self.data_dir):
#             raise FileNotFoundError(f"Data directory '{self.data_dir}' not found")

#         pdf_files = [f for f in os.listdir(self.data_dir) if f.endswith(".pdf")]
#         if not pdf_files:
#             raise ValueError(f"No PDF files found in '{self.data_dir}'")

#         documents = []
#         for pdf_file in pdf_files:
#             pdf_path = os.path.join(self.data_dir, pdf_file)
#             try:
#                 loader = PyPDFLoader(pdf_path)
#                 docs = loader.load()
#                 # Add source metadata
#                 for doc in docs:
#                     doc.metadata["source"] = pdf_file
#                 documents.extend(docs)
#             except Exception as e:
#                 print(f"Error loading {pdf_file}: {e}")

#         return documents

#     def load_urls(self, urls: List[str]) -> List[Document]:
#         """Load documents from URLs as fallback"""
#         try:
#             loader = UnstructuredURLLoader(urls=urls)
#             docs = loader.load()
#             for doc in docs:
#                 doc.metadata["source"] = "web"
#             return docs
#         except Exception as e:
#             print(f"Error loading URLs: {e}")
#             return []

#     def chunk_documents(self, documents: List[Document]) -> List[Document]:
#         """Split documents into chunks"""
#         return self.text_splitter.split_documents(documents)

#     def get_processing_stats(
#         self, documents: List[Document], chunks: List[Document]
#     ) -> ProcessingStats:
#         """Get statistics about document processing"""
#         start_time = time.time()

#         # Count unique sources
#         sources = set()
#         for doc in documents:
#             if "source" in doc.metadata:
#                 sources.add(doc.metadata["source"])

#         processing_time = time.time() - start_time

#         return ProcessingStats(
#             total_documents=len(sources),
#             total_chunks=len(chunks),
#             processing_time=processing_time,
#             last_updated=datetime.now(),
#         )

#     def get_document_info(self, documents: List[Document]) -> List[Dict[str, Any]]:
#         """Get information about processed documents"""
#         doc_info = {}

#         for doc in documents:
#             source = doc.metadata.get("source", "unknown")
#             if source not in doc_info:
#                 doc_info[source] = {
#                     "filename": source,
#                     "page_count": 0,
#                     "chunk_count": 0,
#                 }

#             if "page" in doc.metadata:
#                 doc_info[source]["page_count"] = max(
#                     doc_info[source]["page_count"], doc.metadata["page"]
#                 )

#             doc_info[source]["chunk_count"] += 1

#         return list(doc_info.values())
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
from app.config import settings


def load_and_split_documents() -> List[Document]:
    docs = []
    for file in os.listdir(settings.DOCS_DIR):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(settings.DOCS_DIR, file))
            docs.extend(loader.load())
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    return text_splitter.split_documents(docs)
