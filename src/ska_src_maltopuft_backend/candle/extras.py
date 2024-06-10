"""Extras used by the Candidate Handler."""

from typing import Annotated

from pydantic import StringConstraints

RA_PATTERN = r"^(\d):(\d{2}):(\d{2})\.(\d{2})$"
DEC_PATTERN = r"^(-)?(\d{2}):(\d{2}):(\d{2})\.(\d)$"

RaStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=10,
        max_length=10,
        pattern=RA_PATTERN,
    ),
]

DecStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=10,
        max_length=12,
        pattern=DEC_PATTERN,
    ),
]
