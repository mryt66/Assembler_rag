from datetime import datetime

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str
    gemini_api_key: str = Field(min_length=1)
    history: list[dict] | None = None


class ChatResponse(BaseModel):
    response: str
    timestamp: datetime
