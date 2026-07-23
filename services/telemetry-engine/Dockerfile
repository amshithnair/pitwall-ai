FROM python:3.12-slim as builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY libs/ libs/
COPY services/telemetry-engine/ services/telemetry-engine/

RUN uv sync --frozen --no-dev --package pitwall-telemetry-engine

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "pitwall.telemetry_engine.main:app", "--host", "0.0.0.0", "--port", "8000"]
