from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.database.db import get_db, init_db, Conversation
from app.embeddings.initialize import initialize_system, RAGState
from app.rag.prompt_utils import construct_prompt, format_history
from app.gemini.client import get_answer
from app.schemas import ChatRequest, ChatResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    state = initialize_system()
    app.state.rag_state = state
    yield


app = FastAPI(title="RAG Chat API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    state: RAGState = app.state.rag_state
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
