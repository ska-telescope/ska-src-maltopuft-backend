"""Label controller tests."""

#  ruff: noqa: SLF001, PLR2004


import pytest
import pytest_asyncio
from ska_src_maltopuft_backend.core.factory import Factory
from ska_src_maltopuft_backend.label.controller import LabelController
from sqlalchemy.orm import Session

from tests.api.v1.datagen import label_data_generator
from tests.extras import build_request


@pytest_asyncio.fixture(scope="module")
async def controller() -> LabelController:
    """Label controller fixture."""
    return Factory().get_label_controller()


@pytest.mark.asyncio()
async def test_create_label_with_missing_request_user(
    db: Session,
    controller: LabelController,
) -> None:
    """Attempting to create a label with missing user information in the
    request should raise an AttributeError.
    """
    request_missing_user = build_request(user=None)
    label = label_data_generator()
    with pytest.raises(
        AttributeError,
        match="Request object does not have a user attribute",
    ):
        await controller.create(
            db=db,
            attributes=label,
            request=request_missing_user,
        )


@pytest.mark.asyncio()
async def test_create_many_label_with_missing_request_user(
    db: Session,
    controller: LabelController,
) -> None:
    """Attempting to create many labels with missing user information in the
    request should raise an AttributeError.
    """
    request_missing_user = build_request(user=None)
    labels = [label_data_generator() for _ in range(3)]
    with pytest.raises(
        AttributeError,
        match="Request object does not have a user attribute",
    ):
        await controller.create_many(
            db=db,
            objects=labels,
            request=request_missing_user,
        )
