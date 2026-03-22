import os
from dataclasses import dataclass
import faiss
import numpy as np
from typing import Optional
from sentence_transformers import SentenceTransformer
from config.config import settings
from .loader import load_json, compute_and_cache_embeddings


@dataclass
class RAGState:
    chunks_data: list[dict]
    chunk_embeddings: Optional[np.ndarray]
    faiss_index: Optional[faiss.Index]
    base_chunk: dict
    system_prompt: dict
    model_embedding: SentenceTransformer

    @property
    def chunk_count(self) -> int:
        return len(self.chunks_data)


def initialize_system() -> RAGState:
    model_name = settings.embedding_model or os.getenv(
        "EMBEDDING_MODEL", "Qwen/Qwen3-Embedding-0.6B"
    )
    model = SentenceTransformer(model_name)

    chunks = load_json(settings.output_chunks_file)
    prompt_cfg = load_json(settings.rag_config_file)[0]

    emb, index = compute_and_cache_embeddings(
        chunks=chunks,
        model=model,
        embeddings_file=settings.embeddings_file,
        index_file=settings.faiss_index_file,
    )

    return RAGState(
        chunks_data=chunks,
        chunk_embeddings=emb,
        faiss_index=index,
        base_chunk=prompt_cfg["base_chunk"],
        system_prompt=prompt_cfg["system_prompt"],
        model_embedding=model,
    )
