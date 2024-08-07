"""KnownPulsar response schemas."""

from pydantic import (
    BaseModel,
    ConfigDict,
    PastDatetime,
    PositiveFloat,
    PositiveInt,
)

from ska_src_maltopuft_backend.core.types import DecStr, RaStr


class KnownPulsar(BaseModel):
    """Response model for Candidate HTTP GET/POST requests."""

    # pylint: disable=R0801

    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt
    name: str
    dm: PositiveFloat | None
    width: PositiveFloat | None
    ra: RaStr
    dec: DecStr
    period: PositiveFloat | None
    created_at: PastDatetime
    updated_at: PastDatetime
