"""Label service API tests."""

# ruff: noqa: D103

from typing import Any

from fastapi.testclient import TestClient
from pytest_bdd import given, scenarios, then, when
from ska_src_maltopuft_backend.app.schemas.responses import Label, LabelBulk

scenarios("./label_api.feature")


@given("parent entity is None")
def label_null_parent_entity(result: dict[str, Any]) -> None:
    """Generate fake label data with null parent entity."""
    label = result.get("label")
    assert isinstance(label, dict)
    label["entity_id"] = ""


@given("parent labeller is None")
def label_null_parent_labeller(result: dict[str, Any]) -> None:
    """Generate fake label data with null parent labeller."""
    label = result.get("label")
    assert isinstance(label, dict)
    label["labeller_id"] = ""


@given("parent candidate is None")
def label_null_parent_candidate(result: dict[str, Any]) -> None:
    """Generate fake label data with null parent candidate."""
    label = result.get("label")
    assert isinstance(label, dict)
    label["candidate_id"] = ""


@given("parent entity attribute is non-existent")
def label_non_existent_parent_entity(result: dict[str, Any]) -> None:
    """Generate fake label data with non-existent parent entity."""
    label = result.get("label")
    assert isinstance(label, dict)
    label["entity_id"] = 999


@given("parent labeller attribute is non-existent")
def label_non_existent_parent_labeller(result: dict[str, Any]) -> None:
    """Generate fake label data with non-existent parent entity."""
    label = result.get("label")
    assert isinstance(label, dict)
    label["labeller_id"] = 999


@given("parent candidate attribute is non-existent")
def label_non_existent_parent_candidate(result: dict[str, Any]) -> None:
    """Generate fake label data with non-existent parent candidate."""
    label = result.get("label")
    assert isinstance(label, dict)
    label["candidate_id"] = 999


@given("the labels are combined into one list")
def combine_labels(result: dict[str, Any]) -> None:
    """Combine labels."""
    label = result.get("label")
    assert isinstance(label, dict)
    if result.get("labels") is None:
        result["labels"] = [label]
    else:
        labels = result.get("labels")
        assert isinstance(labels, list)
        labels.append(label)
        result["labels"] = labels


@given("the label is for a candidate which the labeller has already labelled")
def labeller_duplicate_label(
    result: dict[str, Any],
    client: TestClient,
) -> None:
    """Generate a duplicate label."""
    label = result.get("label")
    assert isinstance(label, dict)

    existing_label = client.get(url="/v1/labels/1").json()
    label["candidate_id"] = existing_label.get("candidate_id")
    label["labeller_id"] = existing_label.get("labeller_id")


@when("labels are retrieved from the database")
def do_get_sp_candidates(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.get(url="/v1/labels")


@when("an attempt is made to create the label")
def do_create_label(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.post(
        url="/v1/labels",
        json=result.get("label"),
    )


@when("an attempt is made to create the labels")
def do_create_labels(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.post(
        url="/v1/labels",
        json=result.get("labels"),
    )


@when("the label is retrieved from the database by id")
def do_get_label_by_id(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.get(url="/v1/labels/1")


@then("the response data should contain a label")
def response_data_has_label(result: dict[str, Any]) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    assert data is not None
    label = Label(**data)
    assert label.id is not None


@then("the response data should contain three labels")
def response_data_has_3_labels(result: dict[str, Any]) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    assert data is not None
    assert len(data) == 3  # noqa: PLR2004
    for d in data:
        Label(**d)


@then("the response data should contain three label ids")
def response_data_has_3_label_ids(result: dict[str, Any]) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    data = LabelBulk(**data)
    assert len(data.ids) == 3  # noqa: PLR2004