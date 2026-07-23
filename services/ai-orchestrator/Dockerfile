FROM python:3.12-slim as builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY libs/ libs/
COPY services/ai-orchestrator/ services/ai-orchestrator/

RUN uv sync --frozen --no-dev --package pitwall-ai-orchestrator

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "pitwall.ai_orchestrator.main:app", "--host", "0.0.0.0", "--port", "8000"]
