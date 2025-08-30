import os
import pickle
from typing import List, Dict, Any, Optional
from langchain_community.vectorstores import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from models.rag_models import SearchResult, VectorStoreConfig
import json


class VectorStoreService:
    def __init__(
        self, persist_directory: str = "vectorstore", collection_name: str = "documents"
    ):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore: Optional[Chroma] = None
        self.config_file = os.path.join(persist_directory, "config.json")
        self.stats_file = os.path.join(persist_directory, "stats.pkl")

        # Create directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)

    def initialize_vectorstore(self, documents: List[Document]) -> bool:
        """Initialize vector store with documents"""
        try:
            print(f"Creating vector store with {len(documents)} documents...")

            # Create new vector store
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                collection_name=self.collection_name,
                embedding=self.embeddings,
                persist_directory=self.persist_directory,
            )

            # Save configuration
            self._save_config()

            print("Vector store created successfully!")
            return True

        except Exception as e:
            print(f"Error creating vector store: {e}")
            return False

    def load_existing_vectorstore(self) -> bool:
        """Load existing vector store from disk"""
        try:
            if os.path.exists(os.path.join(self.persist_directory, "chroma.sqlite3")):
                print("Loading existing vector store...")
                self.vectorstore = Chroma(
                    collection_name=self.collection_name,
                    embedding_function=self.embeddings,
                    persist_directory=self.persist_directory,
                )
                print("Vector store loaded successfully!")
                return True
            return False
        except Exception as e:
            print(f"Error loading vector store: {e}")
            return False

    def search_similar(self, query: str, k: int = 3) -> List[SearchResult]:
        """Search for similar documents"""
        if not self.vectorstore:
            raise ValueError("Vector store not initialized")

        try:
            results = self.vectorstore.similarity_search_with_score(query, k=k)

            search_results = []
            for doc, score in results:
                search_result = SearchResult(
                    content=doc.page_content,
                    score=float(score),
                    source=doc.metadata.get("source", "unknown"),
                    metadata=doc.metadata,
                )
                search_results.append(search_result)

            return search_results

        except Exception as e:
            print(f"Error searching vector store: {e}")
            return []

    def get_retriever(self):
        """Get retriever for the vector store"""
        if not self.vectorstore:
            raise ValueError("Vector store not initialized")
        return self.vectorstore.as_retriever()

    def is_initialized(self) -> bool:
        """Check if vector store is initialized"""
        return self.vectorstore is not None

    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the vector store collection"""
        if not self.vectorstore:
            return {"error": "Vector store not initialized"}

        try:
            collection = self.vectorstore._collection
            count = collection.count()

            return {
                "collection_name": self.collection_name,
                "total_documents": count,
                "persist_directory": self.persist_directory,
            }
        except Exception as e:
            return {"error": str(e)}

    def _save_config(self):
        """Save vector store configuration"""
        config = {
            "collection_name": self.collection_name,
            "persist_directory": self.persist_directory,
            "embedding_model": "text-embedding-ada-002",
        }

        try:
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def clear_vectorstore(self):
        """Clear the vector store"""
        try:
            if self.vectorstore:
                self.vectorstore._collection.delete(where={})
                print("Vector store cleared successfully!")
        except Exception as e:
            print(f"Error clearing vector store: {e}")
