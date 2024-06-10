"""Tests for candle extras."""

# ruff: noqa: D103

import re
from typing import Any

import pytest
from pydantic import ValidationError
from pydantic.type_adapter import TypeAdapter
from pytest_bdd import given, parsers, scenarios, then, when

from src.ska_src_maltopuft_backend.candle.extras import (
    DEC_PATTERN,
    RA_PATTERN,
    DecStr,
    RaStr,
)

scenarios("./candle_extras.feature")


@pytest.fixture()
def context() -> dict[str, Any]:
    return {
        "input": str,
        "match": Any,
        "ra_type_adapter": TypeAdapter(RaStr),
        "dec_type_adapter": TypeAdapter(DecStr),
    }


@given(parsers.parse("input value {value} is provided"))
def input_value(context: dict[str, Any], value: Any) -> None:
    context["input"] = value


@given(parsers.parse("valid input value {value} is provided"))
def valid_input_value(context: dict[str, Any], value: Any) -> None:
    context["input"] = value


@given(parsers.parse("invalid input value {value} is provided"))
def invalid_input_value(context: dict[str, Any], value: Any) -> None:
    context["input"] = value


@when("value is pattern matched against the ra regex")
def do_ra_regex(context: dict[str, Any]) -> None:
    pattern = re.compile(RA_PATTERN)
    input_ = context.get("input")
    assert isinstance(input_, str)
    context["match"] = pattern.match(input_)


@when("value is pattern matched against the dec regex")
def do_dec_regex(context: dict[str, Any]) -> None:
    pattern = re.compile(DEC_PATTERN)
    input_ = context.get("input")
    assert isinstance(input_, str)
    context["match"] = pattern.match(input_)


@then(parsers.parse("pattern matching should return {expected}"))
def check_match(context: dict[str, Any], expected: str) -> None:
    if expected == "True":
        assert context.get("match")
    if expected == "None":
        assert context.get("match") is None


@then("validation with RaStr type is successful")
def do_validate_ra_str(context: dict[str, Any]) -> None:
    assert context["ra_type_adapter"].validate_python(context.get("input"))


@then("validation with DecStr type is successful")
def do_validate_dec_str(context: dict[str, Any]) -> None:
    assert context["dec_type_adapter"].validate_python(
        context.get("input"),
    )


@then("validation with RaStr type raises a ValidationError")
def ra_str_raises_validation_error(context: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        context["ra_type_adapter"].validate_python(context.get("input"))


@then("validation with DecStr type raises a ValidationError")
def dec_str_raises_validation_error(context: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        context["dec_type_adapter"].validate_python(context.get("input"))
