from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/replay", tags=["replay"])


class ReplayStartRequest(BaseModel):
    session_id: str
    speed: float = 1.0


class ReplaySpeedRequest(BaseModel):
    speed: float


@router.post("/start")
async def start_replay(req: ReplayStartRequest):
    return {"status": "started", "session_id": req.session_id}


@router.post("/stop")
async def stop_replay():
    return {"status": "stopped"}


@router.post("/pause")
async def pause_replay():
    return {"status": "paused"}


@router.post("/resume")
async def resume_replay():
    return {"status": "resumed"}


@router.post("/speed")
async def set_speed(req: ReplaySpeedRequest):
    return {"status": "speed_updated", "speed": req.speed}
