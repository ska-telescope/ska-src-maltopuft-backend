"""Candidate response schemas."""

from pydantic import BaseModel, ConfigDict, Field, PastDatetime

from .extras import DecStr, RaStr


class Candidate(BaseModel):
    """Response model for Candidate HTTP GET/POST requests."""

    # pylint: disable=R0801

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0)
    dm: float = Field(gt=0)
    snr: float = Field(gt=0)
    width: float = Field(gt=0)
    ra: RaStr
    dec: DecStr
    created_at: PastDatetime
    updated_at: PastDatetime


class SPCandidate(BaseModel):
    """Response model for SPCandidate HTTP GET/POST requests."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0)
    data_path: str
    observed_at: PastDatetime
    candidate_id: int = Field(gt=0)
    created_at: PastDatetime
    updated_at: PastDatetime


class CandidateNested(Candidate):
    """Nest single pulse candidate under candidate if it exists."""

    sp_candidate: SPCandidate | None


class SPCandidateNested(SPCandidate):
    """Nest candidate under single pulse candidate."""

    candidate: Candidate
