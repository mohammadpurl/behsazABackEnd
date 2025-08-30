import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY") or ""
    VECTORSTORE_DIR: str = "vectorstore"
    DOCS_DIR: str = os.path.join(os.path.dirname(__file__), "data")


settings = Settings()
