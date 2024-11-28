"""Tests for candle extras."""

# ruff: noqa: D103, PLR2004

from typing import Any

import pytest
from pydantic import ValidationError
from pydantic.type_adapter import TypeAdapter
from pytest_bdd import given, parsers, scenarios, then
from ska_src_maltopuft_backend.core.types import (
    DeclinationDegrees,
    RightAscensionDegrees,
)

scenarios("./candle.feature")


@pytest.fixture()
def context() -> dict[str, Any]:
    return {
        "input": str,
        "ra_type_adapter": TypeAdapter(RightAscensionDegrees),
        "dec_type_adapter": TypeAdapter(DeclinationDegrees),
    }


@given(parsers.parse("valid input value {value} is provided"))
def valid_input_value(context: dict[str, Any], value: Any) -> None:
    context["input"] = float(value)


@given(parsers.parse("invalid input value {value} is provided"))
def invalid_input_value(context: dict[str, Any], value: Any) -> None:
    context["input"] = float(value)


@then("validation with RightAscensionDegrees type is successful")
def do_validate_ra_str(context: dict[str, Any]) -> None:
    res = context["ra_type_adapter"].validate_python(context.get("input"))
    assert 0 <= res <= 360


@then("validation with DeclinationDegrees type is successful")
def do_validate_dec_str(context: dict[str, Any]) -> None:
    res = context["dec_type_adapter"].validate_python(
        context.get("input"),
    )
    assert -90 <= res <= 90


@then("validation with RightAscensionDegrees type raises a ValidationError")
def ra_str_raises_validation_error(context: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        context["ra_type_adapter"].validate_python(context.get("input"))


@then("validation with DeclinationDegrees type raises a ValidationError")
def dec_str_raises_validation_error(context: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        context["dec_type_adapter"].validate_python(context.get("input"))
