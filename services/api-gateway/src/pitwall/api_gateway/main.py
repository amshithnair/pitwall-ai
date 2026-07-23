import logging
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from pitwall.api_gateway.auth import auth_router, verify_token
from pitwall.api_gateway.websockets import ConnectionManager, stream_redis_events

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
manager = ConnectionManager()
background_task = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting API Gateway...")
    global background_task
    background_task = asyncio.create_task(stream_redis_events(manager))
    yield
    if background_task:
        background_task.cancel()
    logger.info("Shutting down API Gateway...")

app = FastAPI(title="PitWall AI - API Gateway", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str):
    # Authenticate WebSocket connection
    user = verify_token(token)
    if not user:
        await websocket.close(code=1008)
        return
        
    await manager.connect(websocket)
    try:
        while True:
            # Keep alive and receive messages
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
