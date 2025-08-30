from pydantic import BaseModel
from typing import List, Optional


class QuestionRequest(BaseModel):
    question: str
    context_length: Optional[int] = 3


class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: List[str]
    confidence: Optional[float] = None


class DocumentInfo(BaseModel):
    filename: str
    page_count: int
    chunk_count: int


class VectorStoreStatus(BaseModel):
    is_initialized: bool
    document_count: int
    total_chunks: int
    documents: List[DocumentInfo]
