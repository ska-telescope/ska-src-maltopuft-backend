"""Database CRUD operations for the Candidate model."""

from ska_src_maltopuft_backend.app.models import Candidate, SPCandidate
from ska_src_maltopuft_backend.core.repository import BaseRepository


class CandidateRepository(BaseRepository[Candidate]):
    """Database CRUD operations for the Candidate model."""

    def __init__(self) -> None:
        """Initialise a CandidateRepository instance."""
        super().__init__(model=Candidate)


class SPCandidateRepository(BaseRepository[SPCandidate]):
    """Database CRUD operations for the SPCandidate model."""

    def __init__(self) -> None:
        """Initialise an SPCandidateRepository instance."""
        super().__init__(model=SPCandidate)


candidate_repository = CandidateRepository()
sp_candidate_repository = SPCandidateRepository()
