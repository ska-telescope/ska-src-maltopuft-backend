"""External catalogue service request schemas."""

from typing import Annotated

from fastapi import Query
from pydantic import Field, PositiveFloat

from ska_src_maltopuft_backend.core.schemas import (
    CommonQueryParams,
    RaDecPositionBase,
    RaDecPositionQueryParameters,
)
from ska_src_maltopuft_backend.core.types import PositiveList


class GetKnownPulsarQueryParams(
    CommonQueryParams,
    RaDecPositionQueryParameters,
):
    """Query parameters for KnownPulsar model HTTP GET requests."""

    name: list[str | None] = Field(Query(default=[]))
    dm: Annotated[PositiveList[float], None] = Field(Query(default=[]))
    width: Annotated[PositiveList[float], None] = Field(Query(default=[]))
    period: Annotated[PositiveList[float], None] = Field(Query(default=[]))


class CreateKnownPulsar(RaDecPositionBase):
    """Schema for KnownPulsar model HTTP POST requests."""

    name: str
    dm: PositiveFloat
    width: PositiveFloat
    period: PositiveFloat
