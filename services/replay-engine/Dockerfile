FROM python:3.12-slim as builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Change working directory
WORKDIR /app

# Copy the workspace foundation
COPY pyproject.toml uv.lock ./
COPY libs/ libs/
COPY services/replay-engine/ services/replay-engine/

# Sync dependencies using uv
RUN uv sync --frozen --no-dev --package pitwall-replay-engine

FROM python:3.12-slim

WORKDIR /app

# Copy the environment from the builder
COPY --from=builder /app/.venv /app/.venv

# Ensure the virtual environment is in the path
ENV PATH="/app/.venv/bin:$PATH"

# Run the application
CMD ["uvicorn", "pitwall.replay_engine.main:app", "--host", "0.0.0.0", "--port", "8000"]
