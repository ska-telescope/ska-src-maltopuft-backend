"""Database CRUD operations for the User model."""

from ska_src_maltopuft_backend.app.models import User
from ska_src_maltopuft_backend.core.repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Database CRUD operations for the User model."""
