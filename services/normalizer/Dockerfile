FROM python:3.12-slim as builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY libs/ libs/
COPY services/normalizer/ services/normalizer/

RUN uv sync --frozen --no-dev --package pitwall-normalizer

FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "pitwall.normalizer.main:app", "--host", "0.0.0.0", "--port", "8000"]
