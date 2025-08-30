from fastapi import FastAPI
from app.routes import qa

app = FastAPI(title="RAG Question Answering API")

# Include routes
app.include_router(qa.router, prefix="/api", tags=["Q&A"])


@app.get("/")
async def root():
    return {"message": "RAG API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
