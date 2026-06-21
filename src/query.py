import os

import chromadb

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from google import genai


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client_ai = genai.Client(
    api_key=API_KEY
)

DB_PATH = "db"
COLLECTION_NAME = "rag_docs"

embed_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

db_client = chromadb.PersistentClient(
    path=DB_PATH
)

collection = db_client.get_collection(
    COLLECTION_NAME
)


def search_docs(question, k=3):
    query_emb = embed_model.encode(
        question
    ).tolist()

    result = collection.query(
        query_embeddings=[query_emb],
        n_results=k
    )

    return result


def ask_gemini(question, docs, metas):
    context = ""

    for text, meta in zip(docs, metas):
        context += (
            f"\nSource: {meta['source']}"
            f" Page: {meta['page']}\n"
        )

        context += text
        context += "\n\n"

    prompt = f"""
You are a document question answering assistant.

Answer ONLY using the provided context.

If the answer does not exist in the documents, say:

"I could not find the answer in the provided documents."

Context:

{context}

Question:
{question}

Answer:
"""

    response = client_ai.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def ask(question):
    result = search_docs(question)

    docs = result["documents"][0]
    metas = result["metadatas"][0]

    answer = ask_gemini(
        question,
        docs,
        metas
    )

    return answer, metas