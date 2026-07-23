import json
import logging
import asyncio
from typing import List
from fastapi import WebSocket
from pitwall.events.redis_broker import RedisEventSubscriber
import redis

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, message: str):
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                self.disconnect(connection)

async def stream_redis_events(manager: ConnectionManager):
    """Background task to read from Redis and broadcast to websockets."""
    redis_client = redis.Redis(host="redis", port=6379, decode_responses=False)
    subscriber = RedisEventSubscriber(redis_client=redis_client)
    subscriber.subscribe("telemetry_group", "api_gateway_worker")
    
    logger.info("Started streaming Redis events to WebSockets.")
    while True:
        try:
            # Poll events in non-blocking way for asyncio
            # In production, use aioredis, but for milestone we use a small timeout and sleep
            events = subscriber.consume(batch_size=50, timeout_ms=50)
            for event in events:
                # Convert Protobuf PitWallEvent to dict for JSON serialization
                event_dict = {
                    "event_type": event.event_type,
                    "session_id": event.session_id,
                    "race_id": event.race_id,
                    "driver_id": event.driver_id,
                    "timestamp": event.timestamp.isoformat(),
                    # For UI we don't strictly need to unpack every proto field if we just pass the struct
                    # But ideally we parse it. For now, pass a simplified version.
                    "payload": str(event.payload) 
                }
                
                # Very simple serialization for the milestone
                await manager.broadcast(json.dumps(event_dict))
                
            await asyncio.sleep(0.01)
        except Exception as e:
            logger.error(f"Redis stream error: {e}")
            await asyncio.sleep(1)
