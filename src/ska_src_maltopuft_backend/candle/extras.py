"""Extras used by the Candidate Handler."""

from typing import Annotated

from pydantic import StringConstraints

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
