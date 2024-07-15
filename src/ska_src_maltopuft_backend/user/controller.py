"""Data controller for the User model."""

from ska_src_maltopuft_backend.app.models import User
from ska_src_maltopuft_backend.app.schemas.requests import CreateUser
from ska_src_maltopuft_backend.core.controller import BaseController
from ska_src_maltopuft_backend.user.repository import (
    UserRepository,
    user_repository,
)


class UserController(BaseController[User, CreateUser, None]):
    """Data controller for the User model."""

    def __init__(self, user_repository_: UserRepository) -> None:
        """Initalise a UserController instance."""
        super().__init__(
            model=User,
            repository=user_repository,
        )
        self.user_repository = user_repository_


user_controller = UserController(user_repository_=user_repository)
