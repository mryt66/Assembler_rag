from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str
    history: list[dict] | None = None


class ChatResponse(BaseModel):
    response: str
    timestamp: datetime
