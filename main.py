from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import qa

app = FastAPI(title="Simple Q&A API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # در production این را محدود کنید
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(qa.router, prefix="/api", tags=["Q&A"])


@app.get("/")
async def root():
    return {"message": "Simple Q&A API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
