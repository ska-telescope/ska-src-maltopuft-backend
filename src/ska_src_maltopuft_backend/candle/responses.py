"""Candidate response schemas."""

from pydantic import (
    BaseModel,
    ConfigDict,
    PastDatetime,
    PositiveFloat,
    PositiveInt,
)

from ska_src_maltopuft_backend.core.types import (
    DeclinationDegrees,
    RightAscensionDegrees,
)


class Candidate(BaseModel):
    """Response model for Candidate HTTP GET/POST requests."""

    # pylint: disable=R0801

    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt
    dm: PositiveFloat
    snr: PositiveFloat
    width: PositiveFloat
    ra: RightAscensionDegrees
    dec: DeclinationDegrees
    observed_at: PastDatetime
    beam_id: PositiveInt
    created_at: PastDatetime
    updated_at: PastDatetime


class SPCandidate(BaseModel):
    """Response model for SPCandidate HTTP GET/POST requests."""

    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt
    plot_path: str
    candidate_id: PositiveInt
    created_at: PastDatetime
    updated_at: PastDatetime


class CandidateNested(Candidate):
    """Nest single pulse candidate under candidate if it exists."""

    sp_candidate: SPCandidate | None


class SPCandidateNested(SPCandidate):
    """Nest candidate under single pulse candidate."""

    candidate: Candidate
