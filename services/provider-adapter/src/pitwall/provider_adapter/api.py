from fastapi import APIRouter, BackgroundTasks, HTTPException
from pitwall.provider_adapter.loader import HistoricalLoader
from pitwall.provider_adapter.registry import ProviderRegistry
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/provider", tags=["provider"])


class LoadHistoricalRequest(BaseModel):
    provider: str
    year: int
    race_identifier: str
    session_type: str


@router.post("/load-historical")
async def load_historical(req: LoadHistoricalRequest, background_tasks: BackgroundTasks):
    registry = ProviderRegistry()
    if not registry.get_provider(req.provider):
        raise HTTPException(status_code=400, detail="Unknown provider")

    loader = HistoricalLoader()
    background_tasks.add_task(
        loader.load_session, req.provider, req.year, req.race_identifier, req.session_type
    )
    return {"status": "accepted", "message": "Loading started in background"}


@router.get("/registry")
async def get_registry():
    registry = ProviderRegistry()
    return registry.list_providers()
