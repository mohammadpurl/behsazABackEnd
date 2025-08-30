from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class DocumentChunk:
    content: str
    metadata: Dict[str, Any]
    source: str
    page_number: Optional[int] = None


@dataclass
class SearchResult:
    content: str
    score: float
    source: str
    metadata: Dict[str, Any]


@dataclass
class VectorStoreConfig:
    collection_name: str
    chunk_size: int
    chunk_overlap: int
    embedding_model: str
    persist_directory: str


@dataclass
class ProcessingStats:
    total_documents: int
    total_chunks: int
    processing_time: float
    last_updated: datetime
