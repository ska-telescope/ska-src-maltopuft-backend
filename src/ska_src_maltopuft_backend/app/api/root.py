"""REST endpoint paths for root ('/')."""

from fastapi import APIRouter

root_router = APIRouter()


@root_router.get("/")
async def read_root() -> dict:
    """Return a dummy response to the root path (/)."""
    return {"data": "Hello world!"}
