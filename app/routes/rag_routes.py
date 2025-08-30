# from fastapi import APIRouter, HTTPException, Depends
# from typing import List
# from app.schemas.rag_schemas import QuestionRequest, QuestionResponse, VectorStoreStatus
# from app.services.rag_service import RAGService
# from app.models.rag_models import SearchResult

# router = APIRouter(prefix="/rag", tags=["RAG System"])

# # Global RAG service instance
# rag_service = RAGService()


# @router.post("/initialize", response_model=dict)
# async def initialize_rag_system(force_rebuild: bool = False):
#     """Initialize the RAG system"""
#     try:
#         success = rag_service.initialize_system(force_rebuild=force_rebuild)
#         if success:
#             return {
#                 "status": "success",
#                 "message": "RAG system initialized successfully",
#                 "force_rebuild": force_rebuild,
#             }
#         else:
#             raise HTTPException(
#                 status_code=500, detail="Failed to initialize RAG system"
#             )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.post("/ask", response_model=QuestionResponse)
# async def ask_question(request: QuestionRequest):
#     """Ask a question and get an answer"""
#     try:
#         if not rag_service.is_initialized:
#             raise HTTPException(
#                 status_code=400,
#                 detail="RAG system not initialized. Call /initialize first.",
#             )

#         response = rag_service.ask_question(
#             question=request.question, context_length=request.context_length or 3
#         )
#         return response
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.get("/search")
# async def search_documents(query: str, k: int = 5):
#     """Search for relevant documents"""
#     try:
#         if not rag_service.is_initialized:
#             raise HTTPException(
#                 status_code=400,
#                 detail="RAG system not initialized. Call /initialize first.",
#             )

#         results = rag_service.search_documents(query, k)
#         return {
#             "query": query,
#             "results": [
#                 {
#                     "content": result.content,
#                     "score": result.score,
#                     "source": result.source,
#                     "metadata": result.metadata,
#                 }
#                 for result in results
#             ],
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.get("/status", response_model=VectorStoreStatus)
# async def get_system_status():
#     """Get current system status"""
#     try:
#         return rag_service.get_system_status()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.post("/rebuild")
# async def rebuild_vectorstore():
#     """Force rebuild the vector store"""
#     try:
#         success = rag_service.rebuild_vectorstore()
#         if success:
#             return {"status": "success", "message": "Vector store rebuilt successfully"}
#         else:
#             raise HTTPException(
#                 status_code=500, detail="Failed to rebuild vector store"
#             )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.get("/health")
# async def health_check():
#     """Health check endpoint"""
#     return {
#         "status": "healthy",
#         "rag_initialized": rag_service.is_initialized,
#         "service": "RAG API",
#     }
