"""Data controller for the Observation metadata models."""

from ska_src_maltopuft_backend.core.controller import BaseController

from .models import Observation
from .repository import ObservationRepository


class ObservationController(BaseController[Observation, None, None]):
    """Data controller for the Observation model."""

    def __init__(self, repository: ObservationRepository) -> None:
        """Initalise a ObservationController instance."""
        super().__init__(
            model=Observation,
            repository=repository,
        )
        self.repository = repository
