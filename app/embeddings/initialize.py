from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app import config
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
    model_name = os.getenv("EMBEDDING_MODEL", "Qwen/Qwen3-Embedding-0.6B")
    model = SentenceTransformer(model_name)

    chunks = load_json(config.OUTPUT_CHUNKS_FILE)
    prompt_cfg = load_json(config.RAG_CONFIG_FILE)[0]

    emb, index = compute_and_cache_embeddings(
        chunks=chunks,
        model=model,
        embeddings_file=config.EMBEDDINGS_FILE,
        index_file=config.FAISS_INDEX_FILE,
    )

    return RAGState(
        chunks_data=chunks,
        chunk_embeddings=emb,
        faiss_index=index,
        base_chunk=prompt_cfg["base_chunk"],
        system_prompt=prompt_cfg["system_prompt"],
        model_embedding=model,
    )
