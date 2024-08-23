"""Database CRUD operations for the Observation metadata models."""

from ska_src_maltopuft_backend.core.repository import BaseRepository

from .models import Observation


class ObservationRepository(BaseRepository[Observation]):
    """Database CRUD operations for the Observation model."""
