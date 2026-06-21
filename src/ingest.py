import os

import chromadb

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


DB_PATH = "db"
COLLECTION_NAME = "rag_docs"

# Local embedding model
embed_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def read_pdf(path):
    docs = []

    file_name = os.path.basename(path)

    try:
        reader = PdfReader(path)

        for i, page in enumerate(reader.pages):
            text = page.extract_text()

            if text and text.strip():
                docs.append({
                    "text": text.strip(),
                    "source": file_name,
                    "page": i + 1
                })

    except Exception as e:
        print(f"Error reading {file_name}: {e}")

    return docs


def read_txt(path):
    docs = []

    file_name = os.path.basename(path)

    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

            if text.strip():
                docs.append({
                    "text": text,
                    "source": file_name,
                    "page": 1
                })

    except Exception as e:
        print(f"Error reading {file_name}: {e}")

    return docs


def make_chunks(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = []

    for item in docs:
        parts = splitter.split_text(item["text"])

        for text in parts:
            chunks.append({
                "text": text,
                "source": item["source"],
                "page": item["page"]
            })

    return chunks


def save_db(chunks):
    client = chromadb.PersistentClient(path=DB_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    docs = []
    ids = []
    metas = []

    for i, item in enumerate(chunks):
        docs.append(item["text"])

        ids.append(f"doc_{i}")

        metas.append({
            "source": item["source"],
            "page": item["page"]
        })

    print("Creating embeddings...")

    embeds = embed_model.encode(
        docs,
        show_progress_bar=True
    ).tolist()

    collection.add(
        ids=ids,
        documents=docs,
        metadatas=metas,
        embeddings=embeds
    )

    print("Database saved successfully.")


if __name__ == "__main__":
    data_path = "data"

    all_docs = []

    files = os.listdir(data_path)

    for file_name in files:
        path = os.path.join(data_path, file_name)

        if file_name.endswith(".pdf"):
            docs = read_pdf(path)
            all_docs.extend(docs)

        elif file_name.endswith(".txt"):
            docs = read_txt(path)
            all_docs.extend(docs)

    chunks = make_chunks(all_docs)

    print()
    print("Total documents:", len(all_docs))
    print("Total chunks:", len(chunks))
    print()

    save_db(chunks)