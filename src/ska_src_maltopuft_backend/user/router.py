"""Routers for user endpoints."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, status
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from src.ska_src_maltopuft_backend.core.database import get_db

from .controller import user_controller
from .requests import CreateUser, GetUserQueryParams
from .responses import User

logger = logging.getLogger(__name__)
user_router = APIRouter()


@user_router.get(
    "/",
    response_model=list[User],
)
async def get_users(
    q: GetUserQueryParams = Depends(),
    db: Session = Depends(get_db),
) -> Any:
    """Get all users."""
    logger.debug("This is an example log statement.")
    return await user_controller.get_all(db=db, q=q)


@user_router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: PositiveInt,
    db: Session = Depends(get_db),
) -> User:
    """Get user by id."""
    return await user_controller.get_by_id(db=db, id_=user_id)


@user_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
)
async def post_user(user: CreateUser, db: Session = Depends(get_db)) -> User:
    """Create a new user."""
    return await user_controller.create(db=db, attributes=user.model_dump())


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: PositiveInt,
    db: Session = Depends(get_db),
) -> None:
    """Delete user by id."""
    return await user_controller.delete(db=db, id_=user_id)
