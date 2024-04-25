"""Health endpoint response models."""

from enum import Enum

from pydantic import BaseModel


class StatusEnum(str, Enum):
    """Service status values."""

    HEALTHY = "HEALTHY"
    UNAVAILABLE = "UNAVAILABLE"


class Status(BaseModel):
    """Service status response model."""

    name: str
    status: StatusEnum
