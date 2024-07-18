"""Routers for user endpoints."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, status
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from ska_src_maltopuft_backend.core.database.database import get_db
from ska_src_maltopuft_backend.core.factory import Factory

from .controller import UserController
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
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> Any:
    """Get all users."""
    logger.debug("This is an example log statement.")
    return await user_controller.get_all(db=db, q=[q])


@user_router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: PositiveInt,
    db: Session = Depends(get_db),
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> User:
    """Get user by id."""
    return await user_controller.get_by_id(db=db, id_=user_id)


@user_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
)
async def post_user(
    user: CreateUser,
    db: Session = Depends(get_db),
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> User:
    """Create a new user."""
    return await user_controller.create(db=db, attributes=user.model_dump())


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: PositiveInt,
    db: Session = Depends(get_db),
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> None:
    """Delete user by id."""
    return await user_controller.delete(db=db, id_=user_id)
