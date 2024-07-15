"""Extras used in the application."""

from typing import Annotated, TypeVar

from annotated_types import Gt

from ska_src_maltopuft_backend.core.database.base import Base

T = TypeVar("T")
PositiveList = list[Annotated[T, Gt(0)]]

ModelT = TypeVar("ModelT", bound=Base)
CreateModelT = TypeVar("CreateModelT")
UpdateModelT = TypeVar("UpdateModelT")
