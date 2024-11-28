"""Ra and dec types."""

from typing import Annotated, TypeVar

from annotated_types import Ge, Gt, Le
from pydantic import BaseModel

from ska_src_maltopuft_backend.core.database.base import Base

RightAscensionDegrees = Annotated[float, Ge(0), Le(360), lambda x: round(x, 5)]

DeclinationDegrees = Annotated[float, Ge(-90), Le(90), lambda x: round(x, 5)]

T = TypeVar("T")
PositiveList = list[Annotated[T, Gt(0)]]

ModelT = TypeVar("ModelT", bound=Base)
CreateModelT = TypeVar("CreateModelT", bound=BaseModel | None)
UpdateModelT = TypeVar("UpdateModelT", bound=BaseModel | None)
