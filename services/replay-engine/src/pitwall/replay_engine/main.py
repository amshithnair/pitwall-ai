import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pitwall.replay_engine.api import router
from prometheus_client import make_asgi_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Replay Engine...")
    yield
    logger.info("Shutting down Replay Engine...")


app = FastAPI(title="PitWall AI - Replay Engine", lifespan=lifespan)

# Add Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.include_router(router)
