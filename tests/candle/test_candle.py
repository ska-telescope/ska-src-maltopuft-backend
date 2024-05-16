"""Tests for candle sub-package."""

# ruff: noqa: D103

import re
from typing import Any

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from src.ska_src_maltopuft_backend.candle.extras import (
    DEC_PATTERN,
    RA_PATTERN,
)

scenarios("./candle.feature")


@pytest.fixture()
def context() -> dict[str, Any]:
    return {
        "input": str,
        "match": Any,
    }


@given(parsers.parse("input value {value} is provided"))
def input_value(context: dict[str, Any], value: Any) -> None:
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
