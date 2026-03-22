# Assembler RAG API

FastAPI backend providing RAG (Retrieval-Augmented Generation) chat over a knowledge base built from PDF and `.prg` source files. Document chunks are embedded with SentenceTransformer, retrieved via FAISS similarity search, and passed as context to Google Gemini for answer generation. Conversations are persisted in SQLite.

## Features

- RAG pipeline: PDF + `.prg` ingestion → chunk embeddings → FAISS retrieval → Gemini answer generation
- Configurable embedding model (`EMBEDDING_MODEL`)
- Optional Langfuse tracing
- Conversation history in SQLite
- Swagger docs at `/docs`

## Deployment

1. Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

2. Place source PDFs in `data/pdfs/` and `.prg` files in `data/prg/`.

3. Build and run:

```bash
docker compose up --build
```

API available at http://localhost:8000/docs

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `EMBEDDING_MODEL` | No | SentenceTransformer model (default: `Qwen/Qwen3-Embedding-0.6B`) |
| `LANGFUSE_PUBLIC_KEY` | No | Langfuse public key |
| `LANGFUSE_SECRET_KEY` | No | Langfuse secret key |
| `LANGFUSE_HOST` | No | Langfuse host URL |

## Chat API Contract

`POST /chat` requires `gemini_api_key` in the JSON body.

Example payload:

```json
{
	"query": "How does SOZ work?",
	"gemini_api_key": "YOUR_GEMINI_API_KEY",
	"history": [
		{"role": "user", "message": "..."},
		{"role": "assistant", "message": "..."}
	]
}
```

