"""Database CRUD operations for the Label service."""

from ska_src_maltopuft_backend.app.models import Entity, Label
from ska_src_maltopuft_backend.core.repository import BaseRepository


class LabelRepository(BaseRepository[Label]):
    """Database CRUD operations for the Label model."""


class EntityRepository(BaseRepository[Entity]):
    """Database CRUD operations for the Entity model."""
