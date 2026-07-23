import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AI Orchestrator...")
    yield
    logger.info("Shutting down AI Orchestrator...")

app = FastAPI(title="PitWall AI - Orchestrator", lifespan=lifespan)

class ChatRequest(BaseModel):
    message: str
    session_id: str

@app.get("/health")
def health():
    return {"status": "healthy"}
