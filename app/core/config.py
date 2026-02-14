import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
REDIS_URL = os.getenv("REDIS_URL")
API_URL = os.getenv("API_URL", "http://localhost:8001")

# AI Constants
LLM_MODEL_DEFAULT = "gpt-4o"
EXTRACTION_MODEL_DEFAULT = "gpt-3.5-turbo-0125"
EMBEDDING_DIMENSION = 1536

