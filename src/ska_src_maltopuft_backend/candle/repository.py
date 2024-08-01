"""Database CRUD operations for the Candidate model."""

from ska_src_maltopuft_backend.app.models import Candidate, SPCandidate
from ska_src_maltopuft_backend.core.repository import BaseRepository


class CandidateRepository(BaseRepository[Candidate]):
    """Database CRUD operations for the Candidate model."""


class SPCandidateRepository(BaseRepository[SPCandidate]):
    """Database CRUD operations for the SPCandidate model."""
