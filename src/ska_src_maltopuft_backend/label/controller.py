"""Data controller for the Label service models."""

from ska_src_maltopuft_backend.app.models import Entity, Label
from ska_src_maltopuft_backend.core.controller import BaseController
from ska_src_maltopuft_backend.label.repository import (
    EntityRepository,
    LabelRepository,
    entity_repository,
    label_repository,
)


class LabelController(BaseController[Label]):
    """Data controller for the Label model."""

    def __init__(self, repository: LabelRepository) -> None:
        """Initalise a LabelController instance."""
        super().__init__(
            model=Label,
            repository=repository,
        )
        self.repository = repository


class EntityController(BaseController[Entity]):
    """Data controller for the Entity model."""

    def __init__(self, repository: EntityRepository) -> None:
        """Initalise a EntityController instance."""
        super().__init__(
            model=Entity,
            repository=repository,
        )
        self.repository = repository


label_controller = LabelController(repository=label_repository)
entity_controller = EntityController(repository=entity_repository)
