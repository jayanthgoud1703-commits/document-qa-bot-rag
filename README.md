# Document Q&A Bot using RAG

## Project Description

Document Q&A Bot is a Retrieval-Augmented Generation (RAG) application that allows users to ask natural language questions about a collection of documents. The system retrieves relevant document content from a vector database and uses Gemini to generate grounded answers.

The application supports PDF and TXT documents, performs semantic search using embeddings, and provides answers along with source citations. This ensures that responses are based only on the uploaded documents and reduces hallucinations.

---

# Tech Stack

| Technology               | Version | Purpose               |
| ------------------------ | ------- | --------------------- |
| Python                   | 3.11+   | Programming language  |
| ChromaDB                 | 1.x     | Vector database       |
| Sentence Transformers    | 5.x     | Text embeddings       |
| Google GenAI SDK         | Latest  | Answer generation     |
| pypdf                    | 5.x     | PDF text extraction   |
| python-dotenv            | 1.x     | Environment variables |
| langchain-text-splitters | 0.x     | Text chunking         |

---

# Architecture Overview

The system follows a Retrieval-Augmented Generation pipeline.

```text
Documents
    ↓
Document Ingestion
    ↓
Text Chunking
    ↓
Embedding Generation
    ↓
ChromaDB Vector Store
    ↓
Similarity Search
    ↓
Context Retrieval
    ↓
Gemini Answer Generation
    ↓
Grounded Response with Citations
```

### Components

1. Document Ingestion
2. Chunking
3. Embedding
4. Vector Database
5. Retrieval
6. Answer Generation

---

# Chunking Strategy

The application uses Recursive Character Text Splitting.

* Chunk Size: 1000 characters
* Chunk Overlap: 200 characters

This approach helps preserve context between adjacent chunks. The overlap ensures that important information located near chunk boundaries is not lost during retrieval.

Recursive splitting was selected because it produces meaningful chunks while maintaining semantic continuity.

---

# Embedding Model and Vector Database

## Embedding Model

Model Used:

```text
all-MiniLM-L6-v2
```

Reasons for selection:

* Fast inference
* Runs locally
* No API cost
* Lightweight model
* Good semantic search performance

## Vector Database

Database Used:

```text
ChromaDB
```

Reasons for selection:

* Persistent storage
* Simple setup
* Local execution
* Fast similarity search
* No external server requirement

---

# Project Structure

```text
document-qa-bot/
│
├── data/
├── db/
├── src/
│   ├── ingest.py
│   ├── query.py
│   ├── main.py
│
├── .env
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Setup Instructions

## Clone Repository

```bash
git clone <repository-url>

cd document-qa-bot
```

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_api_key_here
```

The API key can be generated from Google AI Studio.

Do not commit the `.env` file to GitHub.

---

# Build Vector Database

Run the ingestion pipeline.

```bash
python src/ingest.py
```

This step:

* Reads documents
* Splits text into chunks
* Generates embeddings
* Stores vectors in ChromaDB

---

# Start the Chatbot

```bash
python src/main.py
```

The application starts an interactive command-line chatbot.

---

# Example Queries

| Question                         | Expected Theme            |
| -------------------------------- | ------------------------- |
| What is artificial intelligence? | Definition of AI          |
| Explain machine learning.        | Machine learning concepts |
| What is Python used for?         | Python applications       |
| What are cloud services?         | Cloud computing concepts  |
| What is supervised learning?     | ML learning techniques    |

---

# Sample Output

```text
Ask: What is artificial intelligence?

Answer:
Artificial intelligence is the simulation of human intelligence in machines.

Sources:
AI.pdf (Page 1)
machine_learning.pdf (Page 2)
```

---

# Known Limitations

* Supports only PDF and TXT files.
* Large documents increase indexing time.
* The system depends on the quality of retrieved chunks.
* Questions outside the document collection cannot be answered.
* Retrieval accuracy depends on the embedding model.

---

# Future Improvements

* Streamlit web interface
* DOCX document support
* Hybrid search methods
* Conversation history
* Improved citation formatting

---

# Author

Jayanth Goud

AI Engineering Internship Assignment
