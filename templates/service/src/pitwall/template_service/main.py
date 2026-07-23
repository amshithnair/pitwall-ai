"""Main entrypoint for the PitWall template service."""
import uvicorn
from fastapi import FastAPI
from pitwall.logging import setup_logging

app = FastAPI(
    title="PitWall AI - Template Service",
    description="A template service for PitWall AI",
    version="0.1.0",
)


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize logging and connections on startup."""
    setup_logging()


@app.get("/health/live", tags=["Health"])
async def liveness() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok"}


@app.get("/health/ready", tags=["Health"])
async def readiness() -> dict[str, str]:
    """Readiness probe."""
    return {"status": "ready"}


def start() -> None:
    """Start the service."""
    uvicorn.run("pitwall.template_service.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
