import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from pitwall.ai_orchestrator.agent import F1EngineeringAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize stateless agent
agent = F1EngineeringAgent()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AI Orchestrator...")
    yield
    logger.info("Shutting down AI Orchestrator...")

app = FastAPI(title="PitWall AI - Orchestrator", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    # In a fully stateless design for the milestone, we pass the message directly.
    # Frontend handles conversation history rendering.
    response = agent.chat(request.message)
    return {"response": response, "session_id": request.session_id}

@app.get("/health")
def health():
    return {"status": "healthy"}
