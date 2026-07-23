import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pitwall.provider_adapter.api import router
from prometheus_client import make_asgi_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Provider Adapter...")
    yield
    logger.info("Shutting down Provider Adapter...")


app = FastAPI(title="PitWall AI - Provider Adapter", lifespan=lifespan)

# Add Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.include_router(router)
