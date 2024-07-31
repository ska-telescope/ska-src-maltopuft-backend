"""Data controller for the Candle models."""

from ska_src_maltopuft_backend.app.models import Candidate, SPCandidate
from ska_src_maltopuft_backend.app.schemas.requests import (
    CreateCandidate,
    CreateSPCandidate,
)
from ska_src_maltopuft_backend.candle.repository import (
    CandidateRepository,
    SPCandidateRepository,
    candidate_repository,
    sp_candidate_repository,
)
from ska_src_maltopuft_backend.core.controller import BaseController


class CandidateController(BaseController[Candidate, CreateCandidate, None]):
    """Data controller for the Candidate model."""

    def __init__(self, repository: CandidateRepository) -> None:
        """Initalise a CandidateController instance."""
        super().__init__(
            model=Candidate,
            repository=repository,
        )
        self.repository = repository


class SPCandidateController(
    BaseController[SPCandidate, CreateSPCandidate, None],
):
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
