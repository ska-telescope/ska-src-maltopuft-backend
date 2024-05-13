"""MALTOPUFT database models."""

from src.ska_src_maltopuft_backend.core.database import Base
from src.ska_src_maltopuft_backend.user.models import User

__all__ = ["Base", "User"]
