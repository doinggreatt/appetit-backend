FROM python:3.12-slim

# Install system dependencies for pjsua and build tools

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY .. /app

WORKDIR /app


RUN uv sync --frozen --no-cache

CMD ["/app/.venv/bin/uvicorn", "config.app:app", "--port", "8080", "--host", "0.0.0.0", "--reload"]