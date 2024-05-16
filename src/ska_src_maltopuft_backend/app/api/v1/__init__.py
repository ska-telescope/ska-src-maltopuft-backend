"""Initialise all API v1 routers."""

from fastapi import APIRouter

from src.ska_src_maltopuft_backend.health.router import health_router
from src.ska_src_maltopuft_backend.user.router import user_router
from src.ska_src_maltopuft_backend.candle.router import candle_router

v1_router = APIRouter()
v1_router.include_router(health_router, tags=["Health check"])
v1_router.include_router(user_router, prefix="/users", tags=["User"])
v1_router.include_router(
    candle_router, prefix="/candle", tags=["Candidate Handler"]
)
