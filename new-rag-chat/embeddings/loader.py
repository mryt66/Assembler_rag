from __future__ import annotations

import json
from pathlib import Path

import faiss  # type: ignore
import numpy as np

from sentence_transformers import SentenceTransformer


def load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {path} not found")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in {path}")


def compute_and_cache_embeddings(
    *,
    chunks: list[dict],
    model: SentenceTransformer,
    embeddings_file: Path,
    index_file: Path,
):
    texts = [c["content"] for c in chunks]

    if embeddings_file.exists():
        emb = np.load(str(embeddings_file))
        if emb.shape[0] != len(texts):
            # mismatch => recompute
            emb = model.encode(texts, convert_to_numpy=True).astype("float32")
            np.save(str(embeddings_file), emb)
    else:
        emb = model.encode(texts, convert_to_numpy=True).astype("float32")
        embeddings_file.parent.mkdir(parents=True, exist_ok=True)
        np.save(str(embeddings_file), emb)

    faiss.normalize_L2(emb)

    if index_file.exists():
        index = faiss.read_index(str(index_file))
        if getattr(index, "ntotal", 0) != emb.shape[0]:
            dim = emb.shape[1]
            index = faiss.IndexFlatIP(dim)
            index.add(emb)
            faiss.write_index(index, str(index_file))
    else:
        dim = emb.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(emb)
        index_file.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(index, str(index_file))

    return emb, index
