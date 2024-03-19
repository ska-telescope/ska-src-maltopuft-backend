"""Initialise all API v1 routers."""

from fastapi import APIRouter

from .health import health_router
from .users import user_router

v1_router = APIRouter()
v1_router.include_router(health_router, tags=["health"])
v1_router.include_router(user_router, prefix="/users", tags=["users"])
