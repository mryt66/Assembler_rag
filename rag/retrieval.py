from __future__ import annotations

import faiss  # type: ignore

from embeddings.initialize import RAGState


def retrieve_relevant_chunks(state: RAGState, query: str, top_k: int = 3) -> list[dict]:
    if state.faiss_index is None or state.chunk_embeddings is None:
        raise RuntimeError("RAG index not initialized")

    model = state.model_embedding
    query_emb = model.encode([query], convert_to_numpy=True).astype("float32")
    faiss.normalize_L2(query_emb)
    k = min(top_k, len(state.chunks_data))
    _, indices = state.faiss_index.search(query_emb, k)
    return [state.chunks_data[i] for i in indices[0]]
