import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

DB_PATH = "db"
COLLECTION_NAME = "rag_docs"