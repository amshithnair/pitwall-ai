FROM python:3.12-slim as builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY libs/ libs/
COPY services/api-gateway/ services/api-gateway/

RUN uv sync --frozen --no-dev --package pitwall-api-gateway

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY libs/ libs/
COPY services/api-gateway/ services/api-gateway/
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "pitwall.api_gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]
