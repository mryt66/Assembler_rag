FROM python:3.10-slim AS base
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Allow embedding model override at build time to bake it into the image (optional)
ARG EMBEDDING_MODEL=Qwen/Qwen3-Embedding-0.6B
ENV EMBEDDING_MODEL=${EMBEDDING_MODEL}
RUN python -c "from sentence_transformers import SentenceTransformer as S, __version__; import os; m=os.getenv('EMBEDDING_MODEL'); print(f'Pre-downloading embedding model: {m}'); S(m)" || echo 'Model pre-download failed (will retry at runtime)'

COPY . .

EXPOSE 8000

CMD uvicorn api:app --host 0.0.0.0 --port 8000
