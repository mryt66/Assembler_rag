from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import os
import numpy as np  # noqa: F401  (for forward ref typing of ndarray)
from sentence_transformers import SentenceTransformer
import faiss  # type: ignore

from .loader import load_json, compute_and_cache_embeddings
import config


@dataclass
class RAGState:
    chunks_data: list[dict]
    chunk_embeddings: Optional["np.ndarray"]
    faiss_index: Optional[faiss.Index]
    base_chunk: dict
    system_prompt: dict
    model_embedding: SentenceTransformer

    @property
    def chunk_count(self) -> int:
        return len(self.chunks_data)


def initialize_system() -> RAGState:
    model_name = os.getenv("EMBEDDING_MODEL", "Qwen/Qwen3-Embedding-0.6B")
    print(f"Loading embedding model: {model_name} ...")
    try:
        model = SentenceTransformer(model_name)
    except Exception as e:  # noqa: BLE001
        fallback = "all-MiniLM-L6-v2"
        if model_name != fallback:
            print(f"Primary model load failed ({e}); falling back to {fallback}")
            model = SentenceTransformer(fallback)
        else:
            raise

    print("Loading chunks & prompt config...")
    chunks_path = config.OUTPUT_CHUNKS_FILE
    prompt_cfg_path = config.RAG_CONFIG_FILE
    chunks = load_json(chunks_path)
    prompt_cfg = load_json(prompt_cfg_path)[0]
    base_chunk = prompt_cfg["base_chunk"]
    system_prompt = prompt_cfg["system_prompt"]

    print(f"Loaded {len(chunks)} chunks")

    emb, index = compute_and_cache_embeddings(
        chunks=chunks,
        model=model,
        embeddings_file=config.EMBEDDINGS_FILE,
        index_file=config.FAISS_INDEX_FILE,
    )

    print("RAG state ready")
    return RAGState(
        chunks_data=chunks,
        chunk_embeddings=emb,
        faiss_index=index,
        base_chunk=base_chunk,
        system_prompt=system_prompt,
        model_embedding=model,
    )
