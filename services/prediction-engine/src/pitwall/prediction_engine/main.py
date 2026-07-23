import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pitwall.prediction_engine.registry.session import engine, Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Prediction Engine...")
    Base.metadata.create_all(bind=engine)
    # Start inference consumer here later
    yield
    logger.info("Shutting down Prediction Engine...")

app = FastAPI(title="PitWall AI - Prediction Engine", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "healthy"}
