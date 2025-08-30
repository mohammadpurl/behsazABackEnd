# import os
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from contextlib import asynccontextmanager
# from app.routes.rag_routes import router as rag_router
# from app.services.rag_service import RAGService

# # Set OpenAI API Key
# os.environ["OPENAI_API_KEY"] = (
#     "your_openai_api_key_here"  # Replace with your actual API key
# )

# # Global RAG service instance
# rag_service = None


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup
#     global rag_service
#     rag_service = RAGService()

#     # Try to initialize RAG system on startup
#     try:
#         print("Initializing RAG system on startup...")
#         success = rag_service.initialize_system()
#         if success:
#             print("RAG system initialized successfully on startup!")
#         else:
#             print(
#                 "Failed to initialize RAG system on startup. Manual initialization required."
#             )
#     except Exception as e:
#         print(f"Error during startup initialization: {e}")
#         print("Manual initialization required.")

#     yield

#     # Shutdown
#     print("Shutting down RAG system...")


# # Create FastAPI app
# app = FastAPI(
#     title="RAG Document Q&A System",
#     description="A Retrieval-Augmented Generation system for answering questions from documents",
#     version="1.0.0",
#     lifespan=lifespan,
# )

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Configure this properly for production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include routers
# app.include_router(rag_router)


# @app.get("/")
# async def root():
#     """Root endpoint"""
#     return {
#         "message": "RAG Document Q&A System",
#         "version": "1.0.0",
#         "docs": "/docs",
#         "health": "/rag/health",
#     }


# @app.get("/docs")
# async def get_docs():
#     """Get API documentation"""
#     return {
#         "message": "API Documentation",
#         "swagger_ui": "/docs",
#         "redoc": "/redoc",
#         "openapi": "/openapi.json",
#     }


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI
from app.routes import qa

app = FastAPI(title="RAG Question Answering API")

# include routes
app.include_router(qa.router, prefix="/api", tags=["Q&A"])
