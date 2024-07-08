"""Database CRUD operations for the Label service."""

from ska_src_maltopuft_backend.app.models import Entity, Label
from ska_src_maltopuft_backend.core.repository import BaseRepository


class LabelRepository(BaseRepository[Label]):
    """Database CRUD operations for the Label model."""

    def __init__(self) -> None:
        """Initialise a Label instance."""
        super().__init__(model=Label)


class EntityRepository(BaseRepository[Entity]):
    """Database CRUD operations for the Entity model."""

    def __init__(self) -> None:
        """Initialise an Entity instance."""
        super().__init__(model=Entity)


label_repository = LabelRepository()
entity_repository = EntityRepository()
