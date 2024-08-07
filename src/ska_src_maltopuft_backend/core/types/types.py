"""Ra and dec types."""

from typing import Annotated, TypeVar

from annotated_types import Gt
from pydantic import BaseModel, StringConstraints

from ska_src_maltopuft_backend.core.database.base import Base

RA_PATTERN = r"^((\d)?(\d))h(\d{2})m(\d{2})\.(\d{2})s$"
DEC_PATTERN = r"^(-)?((\d)?(\d))d(\d{2})m(\d{2})\.(\d)s$"

RaStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=9,
        max_length=12,
        pattern=RA_PATTERN,
    ),
]

DecStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=9,
        max_length=12,
        pattern=DEC_PATTERN,
    ),
]

T = TypeVar("T")
PositiveList = list[Annotated[T, Gt(0)]]

ModelT = TypeVar("ModelT", bound=Base)
CreateModelT = TypeVar("CreateModelT", bound=BaseModel | None)
UpdateModelT = TypeVar("UpdateModelT", bound=BaseModel | None)
