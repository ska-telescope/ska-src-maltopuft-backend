"""Extras used in the label service."""

import string
from typing import Annotated

from pydantic import AfterValidator


def is_css_str(v: str) -> str:
    """Assert a hex color string can be parsed from a string input."""
    v = v.strip()
    v = v.lstrip("#")
    css_str_len = 6
    assert len(v) == css_str_len
    assert all(c in string.hexdigits for c in v)
    return v


CssColorStr = Annotated[str, AfterValidator(is_css_str)]
