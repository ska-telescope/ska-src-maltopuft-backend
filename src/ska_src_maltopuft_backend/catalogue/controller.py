"""Data controllers for the external catalogue models."""

from ska_src_maltopuft_backend.core.controller import BaseController

from .models import KnownPulsar
from .repository import KnownPulsarRepository


class KnownPulsarController(BaseController[KnownPulsarRepository, None, None]):
    """Data controller for the KnownPulsar model."""

    def __init__(self, repository: KnownPulsarRepository) -> None:
        """Initalise a KnownPulsarController instance."""
        super().__init__(
            model=KnownPulsar,
            repository=repository,
        )
        self.repository = repository
