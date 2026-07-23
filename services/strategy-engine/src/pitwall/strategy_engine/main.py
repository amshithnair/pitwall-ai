import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pitwall.strategy_engine.database.session import engine, Base

from pitwall.strategy_engine.consumer import StrategyConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

consumer = StrategyConsumer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Strategy Engine...")
    Base.metadata.create_all(bind=engine)
    consumer.start()
    yield
    consumer.stop()
    logger.info("Shutting down Strategy Engine...")

app = FastAPI(title="PitWall AI - Strategy Engine", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "healthy"}
