"""Common query parameters shared for all database entities."""

from typing import Annotated

from fastapi import Query
from pydantic import (
    BaseModel,
    Field,
    PastDatetime,
    PositiveInt,
    computed_field,
)

from .types import DecStr, PositiveList, RaStr


class RaDecPositionBase(BaseModel):
    """Schema for Ra and Dec attributes."""

    ra: RaStr = Field(...)
    dec: DecStr = Field(...)

    @computed_field  # type: ignore[misc]
    @property
    def pos(self) -> str:
        """Compute the (ra, dec) position tuple."""
        return f"({self.ra},{self.dec})"


class CommonQueryParams(BaseModel):
    """Common query parameters shared for all database entities."""

    id: Annotated[PositiveList[int], None] = Field(Query(default=[]))
    skip: Annotated[int, None] = Field(Query(default=0))
    limit: Annotated[PositiveInt, None] = Field(Query(default=100))
    created_at: list[Annotated[PastDatetime, None]] = Field(Query(default=[]))
    updated_at: list[Annotated[PastDatetime, None]] = Field(Query(default=[]))


class ForeignKeyQueryParams(BaseModel):
    """Foreign key parameters that can be queried in joins."""

    schedule_block_id: Annotated[PositiveList[int], None] = Field(
        Query(default=[]),
    )
    observation_id: Annotated[PositiveList[int], None] = Field(
        Query(default=[]),
    )
    beam_id: Annotated[PositiveList[int], None] = Field(Query(default=[]))
    host_id: Annotated[PositiveList[int], None] = Field(Query(default=[]))
    candidate_id: Annotated[PositiveList[int], None] = Field(Query(default=[]))
    sp_candidate_id: Annotated[PositiveList[int], None] = Field(
        Query(default=[]),
    )
