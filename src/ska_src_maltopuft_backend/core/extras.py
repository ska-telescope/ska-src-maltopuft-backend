"""Extras used in the application."""

from typing import Annotated, TypeVar

from annotated_types import Gt

T = TypeVar("T")
PositiveList = list[Annotated[T, Gt(0)]]
