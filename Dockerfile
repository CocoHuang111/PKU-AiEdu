FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/app/models/hf

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        libgomp1 \
        libsndfile1 \
        libreoffice-writer \
        fonts-noto-cjk \
        pandoc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

COPY . .

RUN mkdir -p /app/data/uploads /app/data/frames /app/data/chroma /app/models/hf \
    && useradd --create-home --uid 10001 app \
    && chown -R app:app /app/data /app/models/hf

USER app

EXPOSE 8010

CMD ["sh", "-c", "python -m alembic upgrade head && exec python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8010 --workers 1"]
