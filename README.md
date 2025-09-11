# RAG Chat API

FastAPI backend providing Retrieval-Augmented Generation (RAG) chat over a local knowledge base built from PDF and `.prg` source files. It embeds document chunks with a SentenceTransformer model, retrieves the most relevant chunks via FAISS, constructs a prompt, and queries Google's Gemini model for responses. Conversations are persisted in SQLite.

## Features
- API-only (no web UI) FastAPI service with automatic Swagger docs (`/docs`).
- RAG pipeline: PDF + `.prg` ingestion -> chunk JSONL -> embeddings (cached) -> FAISS similarity search.
- Configurable embedding model via `EMBEDDING_MODEL` (default `Qwen/Qwen3-Embedding-0.6B`).
- Gemini answer generation (`gemini-2.5-flash`) via `GEMINI_API_KEY`.
- Prompt + context + system/base chunks persisted per conversation (SQLite).
- Dockerfile + docker-compose for containerized deployment.

## Repository Layout
```
api.py                    # FastAPI app
config.py                 # Path + schema config
embeddings/               # Loading & initialization
rag/                      # Retrieval + prompt utils
gemini/                   # Gemini client wrapper
database/                 # DB engine + Conversation model
Data artifacts (mounted in ./data):
  data/output_chunks.jsonl       # Content chunks
  data/rag_prompt_config.jsonl   # System & base prompt config
  data/faiss_index.index         # FAISS index (generated)
  data/chunk_embeddings.npy      # Embeddings (generated)
  data/conversations.db          # SQLite conversation history
  data/pdfs/                     # Source PDFs
  data/prg/                      # Source .prg files
```

## Prerequisites
- Python 3.10+
- Valid Gemini API key in environment: `GEMINI_API_KEY`
- (Optional) Docker & Docker Compose

## Quick Start (Local, Windows PowerShell)
```powershell
# 1. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 2. Set environment variable
$env:GEMINI_API_KEY = 'YOUR_KEY_HERE'

# 3. Place your PDFs in .\data\pdfs and .prg files in .\data\prg

# 4. (Optional) Regenerate chunks (writes output_chunks.jsonl)
python generate_rag_data.py

# 5. Start API (Swagger at http://127.0.0.1:8000/docs)
python api.py
```

### Quick Start (Linux/macOS)
```bash
pip install -r requirements.txt
export GEMINI_API_KEY=YOUR_KEY
python generate_rag_data.py
python api.py
```

## Docker Deployment
Build + run with compose (preferred; mounts `./data` for persistence):
```powershell
# (Optional) pick a lighter embedding model for faster cold start
# set EMBEDDING_MODEL=Qwen/Qwen3-Embedding-0.6B
set GEMINI_API_KEY=YOUR_KEY

docker compose up --build
```
Then visit: http://localhost:8000/docs

## Conversation Storage
SQLite file: `data/conversations.db` (table `conversations`). Each row includes query, response, derived context, system/base chunks, full assembled prompt, and timestamp.

