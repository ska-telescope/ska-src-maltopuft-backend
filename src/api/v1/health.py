"""Routers for health check endpoints."""
from fastapi import APIRouter

health_router = APIRouter()


@health_router.get("/ping")
async def ping() -> dict:
    """Return an OK response to clients."""
    return {"data": "ok"}
