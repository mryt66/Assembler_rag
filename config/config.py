import os
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
from pydantic import BaseModel, Field


class Chunk(BaseModel):
    content: str
    source: str
    tags: list[str] = Field(default_factory=list)
    type: str = "prg"


class Settings:
    def __init__(self) -> None:
        try:
            load_dotenv()
        except Exception:
            pass

        self.base_dir = Path(__file__).resolve().parent.parent
        self.data_dir = self.base_dir / "data"
        self.output_chunks_file = self.data_dir / "output_chunks.jsonl"
        self.rag_config_file = self.data_dir / "rag_prompt_config.jsonl"
        self.faiss_index_file = self.data_dir / "faiss_index.index"
        self.embeddings_file = self.data_dir / "chunk_embeddings.npy"
        self.db_file = self.data_dir / "conversations.db"

        self.gemini_api_key = self._get_env("GEMINI_API_KEY", required=False)
        self.embedding_model = self._get_env(
            "EMBEDDING_MODEL", default="Qwen/Qwen3-Embedding-0.6B"
        )
        self.langfuse_public_key = self._get_env("LANGFUSE_PUBLIC_KEY", required=False)
        self.langfuse_secret_key = self._get_env("LANGFUSE_SECRET_KEY", required=False)
        self.langfuse_host = self._get_env("LANGFUSE_HOST", required=False)

        self.gemini_model = "gemini-2.5-flash"

        self.response_schema: dict[str, Any] = {
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

    def _get_env(
        self,
        name: str,
        default: str | None = None,
        required: bool = False,
    ) -> str | None:
        try:
            value = os.getenv(name, default)
            if required and (value is None or value == ""):
                raise ValueError(f"Environment variable {name} is required")
            return value
        except Exception as exc:
            if required:
                raise RuntimeError(
                    f"Failed to read environment variable {name}"
                ) from exc
            return default


settings = Settings()
BASE_DIR = settings.base_dir
DATA_DIR = settings.data_dir
OUTPUT_CHUNKS_FILE = settings.output_chunks_file
RAG_CONFIG_FILE = settings.rag_config_file
FAISS_INDEX_FILE = settings.faiss_index_file
EMBEDDINGS_FILE = settings.embeddings_file
