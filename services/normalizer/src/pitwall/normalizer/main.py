import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pitwall.normalizer.pipeline import NormalizerPipeline
from prometheus_client import make_asgi_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
pipeline = NormalizerPipeline()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Normalizer Service...")
    pipeline.start()
    yield
    pipeline.stop()
    logger.info("Shutting down Normalizer Service...")


app = FastAPI(title="PitWall AI - Normalizer", lifespan=lifespan)

# Add Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/health")
async def health():
    return {"status": "healthy"}
