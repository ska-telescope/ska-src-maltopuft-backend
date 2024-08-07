"""Candidate response schemas."""

from pydantic import BaseModel, ConfigDict, Field, PastDatetime, PositiveInt

from ska_src_maltopuft_backend.core.types import DecStr, RaStr


class Candidate(BaseModel):
    """Response model for Candidate HTTP GET/POST requests."""

    # pylint: disable=R0801

    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt
    dm: float = Field(gt=0)
    snr: float = Field(gt=0)
    width: float = Field(gt=0)
    ra: RaStr
    dec: DecStr
    beam_id: PositiveInt
    created_at: PastDatetime
    updated_at: PastDatetime


class SPCandidate(BaseModel):
    """Response model for SPCandidate HTTP GET/POST requests."""

    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt
    plot_path: str
    observed_at: PastDatetime
    candidate_id: PositiveInt
    created_at: PastDatetime
    updated_at: PastDatetime


class CandidateNested(Candidate):
    """Nest single pulse candidate under candidate if it exists."""

    sp_candidate: SPCandidate | None


class SPCandidateNested(SPCandidate):
    """Nest candidate under single pulse candidate."""

    candidate: Candidate
