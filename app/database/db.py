from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime
from typing import Generator

from sqlalchemy import Column, DateTime, Integer, Text, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.config import DATA_DIR

DATA_DIR.mkdir(exist_ok=True)

DATABASE_URL = f"sqlite:///{DATA_DIR / 'conversations.db'}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text)
    response = Column(Text)
    context = Column(Text)
    base_context = Column(Text)
    system_prompt = Column(Text)
    full_prompt = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
