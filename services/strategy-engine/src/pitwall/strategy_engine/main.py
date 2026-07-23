import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pitwall.strategy_engine.database.session import engine, Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Strategy Engine...")
    Base.metadata.create_all(bind=engine)
    # Start consumer here later
    yield
    logger.info("Shutting down Strategy Engine...")

app = FastAPI(title="PitWall AI - Strategy Engine", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "healthy"}
