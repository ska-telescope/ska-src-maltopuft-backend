"""Data controller for the Label service models."""

from typing import TYPE_CHECKING, Any

from sqlalchemy.orm import Session

from ska_src_maltopuft_backend.core.controller import BaseController
from ska_src_maltopuft_backend.label.repository import (
    EntityRepository,
    LabelRepository,
)

from .models import Entity, Label
from .requests import CreateEntity, CreateLabel, UpdateLabel

if TYPE_CHECKING:
    from fastapi import Request


class LabelController(BaseController[Label, CreateLabel, UpdateLabel]):
    """Data controller for the Label model."""

    def __init__(self, repository: LabelRepository) -> None:
        """Initalise a LabelController instance."""
        super().__init__(
            model=Label,
            repository=repository,
        )
        self.repository = repository

    async def create(
        self,
        db: Session,
        attributes: dict[str, Any],
        *args: Any,  # noqa: ARG002, pylint: disable=unused-argument
        **kwargs: Any,
    ) -> Label:
        """Create new label with labeller_id."""
        request: Request = kwargs.pop("request")

        if request is None:
            msg = "Request object is required."
            raise ValueError(msg)

        attributes["labeller_id"] = request.user.id
        return await super().create(
            db=db,
            attributes=attributes,
        )

    async def create_many(
        self,
        db: Session,
        objects: list[dict[str, Any]],
        *args: Any,  # noqa: ARG002, pylint: disable=unused-argument
        **kwargs: Any,
    ) -> list[int]:
        """Create a list of labels with labeller_id."""
        request = kwargs.pop("request")

        if request is None:
            msg = "Request object is required."
            raise ValueError(msg)

        labels_with_labeller_id = []
        for obj in objects:
            obj["labeller_id"] = request.user.id
            labels_with_labeller_id.append(obj)

        return await super().create_many(
            db=db,
            objects=labels_with_labeller_id,
        )


class EntityController(BaseController[Entity, CreateEntity, None]):
    """Data controller for the Entity model."""

    def __init__(self, repository: EntityRepository) -> None:
        """Initalise a EntityController instance."""
        super().__init__(
            model=Entity,
            repository=repository,
        )
        self.repository = repository
