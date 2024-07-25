"""Observation service response schemas."""

from pydantic import BaseModel, ConfigDict, PastDatetime, PositiveInt


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

    schedule_block_id: PositiveInt
    schedule_block: ScheduleBlock

    created_at: PastDatetime
    updated_at: PastDatetime
