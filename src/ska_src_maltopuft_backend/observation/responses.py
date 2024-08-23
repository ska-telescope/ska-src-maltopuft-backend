"""Observation service response schemas."""

from pydantic import BaseModel, ConfigDict, PastDatetime, PositiveInt

from ska_src_maltopuft_backend.app.schemas.responses import KnownPulsar
from ska_src_maltopuft_backend.core.types import DecStr, RaStr


class ScheduleBlock(BaseModel):
    """Response model for ScheduleBlock HTTP GET/POST requests."""

    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt

    start_at: PastDatetime
    est_end_at: PastDatetime


class Observation(BaseModel):
    """Response model for Observation HTTP GET/POST requests."""

    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt

    t_min: PastDatetime | None = None
    t_max: PastDatetime | None = None
    s_ra: RaStr
    s_dec: DecStr

    created_at: PastDatetime
    updated_at: PastDatetime


class ObservationSources(BaseModel):
    """Response model for Observation HTTP GET/POST requests."""

    model_config = ConfigDict(from_attributes=True)

    observation: Observation
    sources: list[KnownPulsar]
