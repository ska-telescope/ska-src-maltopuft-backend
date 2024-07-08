"""Unit tests for label feature."""

# ruff: noqa: D103

from typing import Any

import pytest
from pydantic import ValidationError
from pydantic.type_adapter import TypeAdapter
from pytest_bdd import given, parsers, scenarios, then
from ska_src_maltopuft_backend.label.css_color import CssColorStr

scenarios("./label.feature")


@pytest.fixture()
def context() -> dict[str, Any]:
    return {
        "input": str,
        "css_str_type": TypeAdapter(CssColorStr),
    }


@given(parsers.parse("input value {value} is provided"))
def input_value(context: dict[str, Any], value: Any) -> None:
    context["input"] = value


@then("validation with CssColorStr type is successful")
def do_validate_valid_css_str(context: dict[str, Any]) -> None:
    assert context["css_str_type"].validate_python(context.get("input"))


@then("validation with CssColorStr type is unsuccessful")
def do_validate_invalid_css_str(context: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        context["css_str_type"].validate_python(context.get("input"))
