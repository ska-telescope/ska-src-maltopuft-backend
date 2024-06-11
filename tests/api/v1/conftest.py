"""BDD test steps shared between API feature tests."""

from typing import Any

import pytest
from fastapi import status
from httpx import Response
from pytest_bdd import given, then


@pytest.fixture()
def result() -> dict[str, Any]:
    """HTTP response fixture to share between 'given', 'when', 'then' steps."""
    return {}


@given("an empty database")
def db_is_empty() -> None:
    """Nothing exists in the database."""
    return


@then("a response should be returned")
def result_is_response(result: dict[str, Any]) -> None:
    """Verify API returned a Response object."""
    res = result.get("result")
    assert isinstance(res, Response)
    result["response"] = res


@then("an error response should be returned")
def result_is_error_response(result: dict[str, Any]) -> None:
    """Verify API returned an error response, which contains only 'message'
    and 'detail' fields.
    """
    response = result.get("result")
    assert response is not None
    response = response.json()
    assert response.get("message") is not None
    assert response.get("status_code") is not None
    result["response"] = response


@then("a validation error response should be returned")
def result_is_validation_error_response(result: dict[str, Any]) -> None:
    """Verify API returned a validation error response, which contains only a
    'detail' field.
    """
    response = result.get("result")
    assert response is not None
    response = response.json()
    assert response.get("detail") is not None
    result["response"] = response


@then("the response data should contain an empty list")
def response_data_is_empty_list(result: dict[str, Any]) -> None:
    """Verify the response data contains an empty list."""
    response = result.get("response")
    assert response is not None
    assert response.json() == []


@then("the response data should be empty")
def response_data_is_empty(result: dict[str, Any]) -> None:
    """Verify the response data is empty/null/None."""
    response = result.get("response")
    assert response is not None
    response = response.json()
    assert response.json() is None


@then("the response data should not be empty")
def response_data_is_not_empty(result: dict[str, Any]) -> None:
    """Verify the response data is not empty/null/None."""
    response = result.get("response")
    assert response is not None
    assert response.json() is not None


@then("the status code should be HTTP 200")
def response_status_code_200(result: dict[str, Any]) -> None:
    """Verify the API response has status code 200."""
    response = result.get("response")
    assert response is not None
    assert response.status_code == status.HTTP_200_OK


@then("the status code should be HTTP 201")
def response_status_code_201(result: dict[str, Any]) -> None:
    """Verify the API response has status code 201."""
    response = result.get("response")
    assert response is not None
    assert response.status_code == status.HTTP_201_CREATED


@then("the status code should be HTTP 204")
def response_status_code_204(result: dict[str, Any]) -> None:
    """Verify the API response has status code 204."""
    response = result.get("response")
    assert response is not None
    assert response.status_code == status.HTTP_204_NO_CONTENT


@then("the status code should be HTTP 404")
def response_status_code_404(result: dict[str, Any]) -> None:
    """Verify the API response has status code 404."""
    response = result.get("response")
    assert response is not None
    assert response.get("status_code") == status.HTTP_404_NOT_FOUND


@then("the status code should be HTTP 409")
def response_status_code_409(result: dict[str, Any]) -> None:
    """Verify the API response has status code 409."""
    response = result.get("response")
    assert response is not None
    assert response.get("status_code") == status.HTTP_409_CONFLICT


@then("the status code should be HTTP 422")
def response_status_code_422(result: dict[str, Any]) -> None:
    """Verify the API response has status code 422."""
    validation_error_response = result.get("result")
    assert validation_error_response is not None
    assert (
        validation_error_response.status_code
        == status.HTTP_422_UNPROCESSABLE_ENTITY
    )
