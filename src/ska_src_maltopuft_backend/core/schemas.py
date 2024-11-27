"""Common query parameters shared for all database entities."""

from typing import Annotated

from fastapi import Query
from pydantic import (
    BaseModel,
    Field,
    PastDatetime,
    PositiveFloat,
    PositiveInt,
    ValidationError,
    ValidationInfo,
    computed_field,
    field_validator,
)

from .types import DeclinationDegrees, PositiveList, RightAscensionDegrees


class RaDecPositionBase(BaseModel):
    """Schema for Ra and Dec attributes."""

    ra: RightAscensionDegrees = Field(...)
    dec: DeclinationDegrees = Field(...)

    @computed_field  # type: ignore[misc]
    @property
    def pos(self) -> str:
        """Compute the (ra, dec) position tuple."""
        return f"({self.ra},{self.dec})"


class RaDecPositionQueryParameters(BaseModel):
    """Query parameters for Ra and Dec attributes used in cone searches."""

    ra: RightAscensionDegrees | None = None
    dec: DeclinationDegrees | None = None
    radius: PositiveFloat | None = None

    @computed_field  # type: ignore[misc]
    @property
    def pos(self) -> str:
        """Compute the (ra, dec) position tuple."""
        return f"({self.ra},{self.dec})"

    @field_validator("radius", mode="before")
    @classmethod
    def validate_one_field_using_the_others(
        cls,
        radius: float | None,
        values: ValidationInfo,
    ) -> float | None:
        """Validates that ra, dec and radius either all have values or are
        all None.
        """
        ra = values.data.get("ra")
        dec = values.data.get("dec")
        ra_or_dec_is_none = ra is None or dec is None

        msg = (
            "Ra, dec and radius parameters are required if one of ra, dec "
            "and radius are provided"
        )
        if radius is None and not ra_or_dec_is_none:
            raise ValidationError(msg)
        if radius and ra_or_dec_is_none:
            raise ValidationError(msg)
        return radius


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
