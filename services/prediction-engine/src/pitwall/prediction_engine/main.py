import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pitwall.prediction_engine.registry.session import engine, Base

from pitwall.prediction_engine.inference.consumer import PredictionConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

consumer = PredictionConsumer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Prediction Engine...")
    Base.metadata.create_all(bind=engine)
    consumer.start()
    yield
    consumer.stop()
    logger.info("Shutting down Prediction Engine...")

app = FastAPI(title="PitWall AI - Prediction Engine", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "healthy"}
