"""Database CRUD operations for external catalogue models."""

from ska_src_maltopuft_backend.core.repository import BaseRepository

from .models import KnownPulsar


class KnownPulsarRepository(BaseRepository[KnownPulsar]):
    """Database CRUD operations for the KnownPulsar model."""
