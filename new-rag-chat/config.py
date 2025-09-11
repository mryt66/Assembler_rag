from __future__ import annotations

from pathlib import Path
from pydantic import BaseModel
from typing import List


# ----- Paths / files -----
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# JSONL files moved under data/ directory
OUTPUT_CHUNKS_FILE = DATA_DIR / "output_chunks.jsonl"
RAG_CONFIG_FILE = DATA_DIR / "rag_prompt_config.jsonl"
FAISS_INDEX_FILE = DATA_DIR / "faiss_index.index"
EMBEDDINGS_FILE = DATA_DIR / "chunk_embeddings.npy"


class Chunk(BaseModel):
    content: str
    source: str
    tags: List[str] = []
    type: str = "prg"


class Settings:
    response_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Text of the chunk (100-500 words, do not cut mid-sentence/paragraph/table)",
                },
                "source": {"type": "string", "description": "PDF filename"},
                "tags": {"type": "array", "items": {"type": "string"}},
                "type": {
                    "type": "string",
                    "description": "Chunk type",
                    "default": "prg",
                },
            },
            "required": ["content", "source", "tags", "type"],
        },
    }
