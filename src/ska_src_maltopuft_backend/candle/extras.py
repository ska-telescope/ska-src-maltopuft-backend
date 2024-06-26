"""Extras used by the Candidate Handler."""

from typing import Annotated

from pydantic import StringConstraints

RA_PATTERN = r"^((\d)?(\d)):(\d{2}):(\d{2})\.(\d{2})$"
DEC_PATTERN = r"^(-)?((\d)?(\d)):(\d{2}):(\d{2})\.(\d)$"

RaStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=9,
        max_length=11,
        pattern=RA_PATTERN,
    ),
]

DecStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=9,
        max_length=11,
        pattern=DEC_PATTERN,
    ),
]
