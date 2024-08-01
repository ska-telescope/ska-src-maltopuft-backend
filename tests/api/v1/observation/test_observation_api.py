"""User service API tests."""

# ruff: noqa: D103, PLR2004

from typing import Any

from pytest_bdd import parsers, scenarios, then
from ska_src_maltopuft_backend.observation.responses import Observation

scenarios("./observation_api.feature")


@then(parsers.parse("the response data should contain {num:d} observations"))
def response_data_has_num_obs(result: dict[str, Any], num: int) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    assert data is not None

    if isinstance(data, dict):
        data = [data]

    assert len(data) == int(num)
    for d in data:
        obs = Observation(**d)
        assert obs.id is not None
