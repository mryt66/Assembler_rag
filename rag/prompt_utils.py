from __future__ import annotations

from embeddings.initialize import RAGState
from .retrieval import retrieve_relevant_chunks


def format_history(history: list[dict] | None, max_turns: int = 6) -> str:
    if not history:
        return ""
    recent = history[-max_turns:]
    lines = []
    for turn in recent:
        role = turn.get("role", "user")
        msg = (turn.get("message") or turn.get("content") or "").strip()
        if not msg:
            continue
        prefix = "User" if role == "user" else "Assistant"
        lines.append(f"{prefix}: {msg}")
    return "\n".join(lines)


def construct_prompt(state: RAGState, query: str, history_text: str = ""):
    relevant = retrieve_relevant_chunks(state, query)
    context = "\n\n".join(c["content"] for c in relevant)
    full = (
        f"System prompt:\n{state.system_prompt['content']}\n\n"
        f"Context:\n{context}\n\n"
        f"{state.base_chunk['content']}\n\n"
    )
    if history_text:
        full += f"Recent conversation:\n{history_text}\n\n"
    full += f"Query:\n{query}"
    return full, context
