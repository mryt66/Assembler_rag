from __future__ import annotations

from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool
import uvicorn

from database.db import get_db, init_db, Conversation
from embeddings.initialize import initialize_system, RAGState
from rag.prompt_utils import construct_prompt, format_history
from gemini.client import get_answer


class ChatResponse(BaseModel):
    response: str
    timestamp: datetime


class ChatRequest(BaseModel):
    query: str
    history: list[dict] | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting RAG Chat API (modular)...")
    init_db()
    try:
        state = initialize_system()
        app.state.rag_state = state
        print(f"✅ Initialized with {state.chunk_count} chunks")
    except Exception as e:  # noqa: BLE001
        print(f"❌ Initialization failed: {e}")
        raise
    yield
    print("Shutting down API...")


app = FastAPI(
    title="RAG Chat API", description="Modular RAG backend", lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest, db: Session = Depends(get_db)):
    state: RAGState = app.state.rag_state  # type: ignore[attr-defined]
    query = (payload.query or "").strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    history_text = format_history(payload.history)
    full_prompt, context = construct_prompt(state, query, history_text)
    answer = await run_in_threadpool(get_answer, full_prompt)
    if not answer:
        answer = "Sorry, I failed to get a response from Gemini. Please try again."

    convo = Conversation(
        query=query,
        response=answer,
        context=context,
        base_context=state.base_chunk["content"],
        system_prompt=state.system_prompt["content"],
        full_prompt=full_prompt,
    )
    try:
        db.add(convo)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    return ChatResponse(response=answer, timestamp=convo.timestamp)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
