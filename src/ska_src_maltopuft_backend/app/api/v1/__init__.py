"""Initialise all API v1 routers."""

from fastapi import APIRouter

from src.ska_src_maltopuft_backend.health.router import health_router
from src.ska_src_maltopuft_backend.user.router import user_router

v1_router = APIRouter()
v1_router.include_router(health_router, tags=["health"])
v1_router.include_router(user_router, prefix="/users", tags=["users"])
