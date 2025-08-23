FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY .. /app

WORKDIR /app


RUN uv sync --frozen --no-cache

CMD ["/app/.venv/bin/uvicorn", "config.app:app", "--port", "8080", "--host", "0.0.0.0", "--reload"]