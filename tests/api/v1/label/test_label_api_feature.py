"""Label service API tests."""

# ruff: noqa: D103, PLR2004

from typing import Any

from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenarios, then, when
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


@given("an updated label")
def updated_label_data(
    result: dict[str, Any],
    client: TestClient,
) -> None:
    """Generate an updated label."""
    label = result.get("label")
    assert isinstance(label, dict)

    existing_label = client.get(url="/v1/labels/1").json()
    update_entities = [1, 2, 3]
    update_entities = [
        ent
        for ent in update_entities
        if ent != existing_label.get("entity_id")
    ]
    label["entity_id"] = update_entities[0]


@when("labels are retrieved from the database")
def do_get_sp_candidates(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.get(url="/v1/labels", params=result.get("q"))


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


@when("an attempt is made to update the label")
def do_update_label(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.put(
        url="/v1/labels/1",
        json=result.get("label"),
    )


@then(parsers.parse("the response data should contain {num:d} labels"))
def response_data_has_num_labels(result: dict[str, Any], num: int) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    assert data is not None

    if isinstance(data, dict):
        data = [data]

    assert len(data) == int(num)
    for d in data:
        label = Label(**d)
        assert label.id is not None


@then("the response data should contain 3 label ids")
def response_data_has_3_label_ids(result: dict[str, Any]) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    data = LabelBulk(**data)
    assert len(data.ids) == 3


@then("the response data should contain the updated data")
def response_data_is_updated_label(result: dict[str, Any]) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()

    updated_data = result.get("label")
    assert isinstance(updated_data, dict)
    for k in updated_data:
        assert data.get(k) == updated_data.get(k)
