"""Routers for Label service endpoints."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, status
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from ska_src_maltopuft_backend.core.database.database import get_db
from ska_src_maltopuft_backend.core.factory import Factory

from .controller import EntityController, LabelController
from .requests import (
    CreateEntity,
    CreateLabel,
    GetEntityQueryParams,
    GetLabelQueryParams,
    UpdateLabel,
)
from .responses import Entity, Label, LabelBulk

logger = logging.getLogger(__name__)
label_router = APIRouter()


@label_router.get(
    "/entity",
    response_model=list[Entity],
)
async def get_entities(
    q: GetEntityQueryParams = Depends(),
    db: Session = Depends(get_db),
    entity_controller: EntityController = Depends(
        Factory().get_entity_controller,
    ),
) -> Any:
    """Get all entities."""
    logger.info(f"Getting all Entities with query parameters {q}")
    return await entity_controller.get_all(db=db, q=[q])


@label_router.get(
    "/entity/{entity_id}",
    response_model=Entity,
)
async def get_entity(
    entity_id: PositiveInt,
    db: Session = Depends(get_db),
    entity_controller: EntityController = Depends(
        Factory().get_entity_controller,
    ),
) -> Entity:
    """Get entity by id."""
    logger.info(f"Getting Entity with id={entity_id}")
    return await entity_controller.get_by_id(db=db, id_=entity_id)


@label_router.post(
    "/entity",
    response_model=Entity,
    status_code=status.HTTP_201_CREATED,
)
async def post_entity(
    entity: CreateEntity,
    db: Session = Depends(get_db),
    entity_controller: EntityController = Depends(
        Factory().get_entity_controller,
    ),
) -> Entity:
    """Create a new entity."""
    logger.info(f"Creating Entity with type={entity.type}")
    return await entity_controller.create(
        db=db,
        attributes=entity.model_dump(),
    )


@label_router.get(
    "/",
    response_model=list[Label],
)
async def get_labels(
    q: GetLabelQueryParams = Depends(),
    db: Session = Depends(get_db),
    label_controller: LabelController = Depends(
        Factory().get_label_controller,
    ),
) -> Any:
    """Get all labels."""
    logger.info(f"Getting all Labels with query parameters {q}")
    return await label_controller.get_all(db=db, q=[q])


@label_router.get(
    "/{label_id}",
    response_model=Label,
)
async def get_label(
    label_id: PositiveInt,
    db: Session = Depends(get_db),
    label_controller: LabelController = Depends(
        Factory().get_label_controller,
    ),
) -> Label:
    """Get label by id."""
    logger.info(f"Getting Label with id={label_id}")
    return await label_controller.get_by_id(db=db, id_=label_id)


@label_router.post(
    "/",
    response_model=Label | LabelBulk,
    status_code=status.HTTP_201_CREATED,
)
async def post_labels(
    labels: CreateLabel | list[CreateLabel],
    db: Session = Depends(get_db),
    label_controller: LabelController = Depends(
        Factory().get_label_controller,
    ),
) -> Label | LabelBulk:
    """Create a new label(s)."""
    if isinstance(labels, list):
        logger.info(f"Creating {len(labels)} Labels")
        created_label_ids = await label_controller.create_many(
            db=db,
            objects=labels,
        )
        return LabelBulk(ids=created_label_ids)

    logger.info(f"Creating Label with candidate_id={labels.candidate_id}")
    return await label_controller.create(
        db=db,
        attributes=labels.model_dump(),
    )


@label_router.put("/{label_id}", response_model=Label)
async def update_item(
    label_id: PositiveInt,
    label: UpdateLabel,
    db: Session = Depends(get_db),
    label_controller: LabelController = Depends(
        Factory().get_label_controller,
    ),
) -> Any:
    """Update a label."""
    existing_label = await label_controller.get_by_id(db=db, id_=label_id)
    return await label_controller.update(
        db=db,
        db_obj=existing_label,
        update_obj=label,
    )
