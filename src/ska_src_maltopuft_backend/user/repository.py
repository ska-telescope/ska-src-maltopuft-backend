"""Database CRUD operations for the User model."""

from src.ska_src_maltopuft_backend.app.models import User
from src.ska_src_maltopuft_backend.core.repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Database CRUD operations for the User model."""

    def __init__(self) -> None:
        """Initialise a UserRepository instance."""
        super().__init__(model=User)


user_repository = UserRepository()
