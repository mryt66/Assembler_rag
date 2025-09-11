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
# 1. Create & activate virtual env (optional but recommended)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3. Set environment variables
$env:GEMINI_API_KEY = 'YOUR_KEY_HERE'
# Optional lighter embedding model (faster first run)
# $env:EMBEDDING_MODEL = 'Qwen/Qwen3-Embedding-0.6B'

# 4. Place your PDFs in .\data\pdfs and .prg files in .\data\prg

# 5. (Optional) Regenerate chunks (writes output_chunks.jsonl)
# Adjust generate_rag_data.py if you want to output into data/ directly
python generate_rag_data.py
# Move or copy the generated output_chunks.jsonl into .\data if needed.

# 6. Start API (Swagger at http://127.0.0.1:8000/docs)
python api.py
```

### Quick Start (Linux/macOS)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GEMINI_API_KEY=YOUR_KEY
# export EMBEDDING_MODEL=Qwen/Qwen3-Embedding-0.6B
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

### Plain Docker
```powershell
set GEMINI_API_KEY=YOUR_KEY

docker build -t rag-chat-api .
docker run -p 8000:8000 -e GEMINI_API_KEY=$env:GEMINI_API_KEY -v ${PWD}\data:/app/data rag-chat-api
```

## Environment Variables
| Name | Required | Default | Description |
|------|----------|---------|-------------|
| GEMINI_API_KEY | Yes | (none) | Google Gemini API key |
| EMBEDDING_MODEL | No | Qwen/Qwen3-Embedding-0.6B | SentenceTransformer model to use |

## Data Pipeline
1. Put source PDFs into `data/pdfs/` and `.prg` files into `data/prg/`.
2. Run `generate_rag_data.py` to produce `output_chunks.jsonl` (currently saved at repo root; move it to `data/` if not already there).
3. Create `data/rag_prompt_config.jsonl` with a JSON array containing at least one object holding `base_chunk` and `system_prompt` fields (already provided/editable).
4. On first API start:
   - Embeddings computed & cached to `data/chunk_embeddings.npy`.
   - FAISS index saved to `data/faiss_index.index`.
   Subsequent starts reuse cached artifacts unless chunk count mismatches.

## API Overview
| Method | Path      | Description |
|--------|-----------|-------------|
| GET    | /health   | Liveness check |
| POST   | /chat     | RAG chat inference |
| GET    | /docs     | Swagger UI |
| GET    | /openapi.json | OpenAPI spec |

### POST /chat Request
```json
{
  "query": "Explain interrupts in simple terms",
  "history": [
    {"role": "user", "message": "Hi"},
    {"role": "assistant", "message": "Hello!"}
  ]
}
```

### Response
```json
{
  "response": "...model answer...",
  "timestamp": "2025-09-11T18:42:03.123456"
}
```

### curl Example
```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is NWD algorithm?"}'
```

## Conversation Storage
SQLite file: `data/conversations.db` (table `conversations`). Each row includes query, response, derived context, system/base chunks, full assembled prompt, and timestamp.

## Updating Content
1. Add/change PDFs / `.prg` files.
2. Regenerate `output_chunks.jsonl` (or append manually in correct JSON array format if small edits).
3. Delete `data/chunk_embeddings.npy` and `data/faiss_index.index` to force full recompute (or just change chunk count and app will rebuild automatically).
4. Restart API.

## Changing the Embedding Model
- Set `EMBEDDING_MODEL` env before startup.
- Delete existing embedding cache/index to avoid dimensionality mismatch.
- Re-run the service (model auto-downloaded). The Dockerfile pre-download stage may fail gracefully and retry at runtime.

## Troubleshooting
| Symptom | Cause | Fix |
|---------|-------|-----|
| Slow first startup | Large embedding model download | Ensure network access or pre-build image |
| `GEMINI_API_KEY not set` | Missing env | Export/set the variable |
| Empty / irrelevant answers | Missing or empty `output_chunks.jsonl` / prompt config | Verify files exist in `data/` |
| Index size mismatch after editing chunks | Cache stale | Delete `chunk_embeddings.npy` + `faiss_index.index` |
| 500 on /chat | DB write or Gemini failure | Check container logs; ensure writable `data/` volume |

## Development Notes
- Docstring headers were intentionally removed per project requirement.
- `Conversation` ORM model now lives in `database/db.py` (merged from `models.py`).
- Adjust `generate_rag_data.py` if you want it to write directly into `data/output_chunks.jsonl`.

## Next Ideas
- Add streaming responses.
- Add rate limiting & auth.
- Add eval script for retrieval quality.
- Add CLI ingestion pipeline & chunk validation.

---
Happy hacking! Open an issue or extend as needed.
