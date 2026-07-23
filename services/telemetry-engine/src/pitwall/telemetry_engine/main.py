import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from prometheus_client import make_asgi_app

from pitwall.telemetry_engine.consumer import TelemetryConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

consumer = TelemetryConsumer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Telemetry & Analytics Engine...")
    consumer.start()
    yield
    consumer.stop()
    logger.info("Shutting down Engine...")

app = FastAPI(title="PitWall AI - Telemetry Engine", lifespan=lifespan)
app.mount("/metrics", make_asgi_app())

@app.get("/health")
async def health():
    return {"status": "healthy"}
