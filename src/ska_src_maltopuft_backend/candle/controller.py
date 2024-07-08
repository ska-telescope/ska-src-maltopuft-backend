"""Data controller for the Candle models."""

from src.ska_src_maltopuft_backend.app.models import Candidate, SPCandidate
from src.ska_src_maltopuft_backend.candle.repository import (
    CandidateRepository,
    SPCandidateRepository,
    candidate_repository,
    sp_candidate_repository,
)
from src.ska_src_maltopuft_backend.core.controller import BaseController


class CandidateController(BaseController[Candidate]):
    """Data controller for the Candidate model."""

    def __init__(self, repository: CandidateRepository) -> None:
        """Initalise a CandidateController instance."""
        super().__init__(
            model=Candidate,
            repository=repository,
        )
        self.repository = repository


class SPCandidateController(BaseController[SPCandidate]):
    """Data controller for the SPCandidate model."""

    def __init__(self, repository: SPCandidateRepository) -> None:
        """Initalise a SPCandidateController instance."""
        super().__init__(
            model=SPCandidate,
            repository=repository,
        )
        self.repository = repository


candidate_controller = CandidateController(repository=candidate_repository)
sp_candidate_controller = SPCandidateController(
    repository=sp_candidate_repository,
)
