"""Routers for user endpoints."""

import logging

from fastapi import APIRouter

from src.ska_src_maltopuft_backend.app.schemas.responses.user import User

logger = logging.getLogger(__name__)
user_router = APIRouter()


@user_router.post("/")
async def post_user(user: User) -> dict:
    """Return the information POSTed by a user back to the client for
    testing.
    """
    logger.debug("This is an example log statement.")
    return {"name": f"{user.name}"}
