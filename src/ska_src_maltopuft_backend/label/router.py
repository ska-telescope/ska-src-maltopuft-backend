"""Routers for Label service endpoints."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, status
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from src.ska_src_maltopuft_backend.core.database import get_db
from src.ska_src_maltopuft_backend.label.controller import (
    entity_controller,
    label_controller,
)
from src.ska_src_maltopuft_backend.label.requests import (
    CreateEntity,
    CreateLabel,
    GetEntityQueryParams,
    GetLabelQueryParams,
)
from src.ska_src_maltopuft_backend.label.responses import Entity, Label

logger = logging.getLogger(__name__)
label_router = APIRouter()


@label_router.get("/entity", response_model=list[Entity])
async def get_entities(
    q: GetEntityQueryParams = Depends(),
    db: Session = Depends(get_db),
) -> Any:
    """Get all entities."""
    return await entity_controller.get_all(db=db, q=q)


@label_router.get("/entity/{entity_id}")
async def get_entity(
    entity_id: PositiveInt,
    db: Session = Depends(get_db),
) -> Entity:
    """Get candle by id."""
    return await entity_controller.get_by_id(db=db, id_=entity_id)


@label_router.post("/entity", status_code=status.HTTP_201_CREATED)
async def post_entity(
    entity: CreateEntity,
    db: Session = Depends(get_db),
) -> Entity:
    """Create a new entity."""
    return await entity_controller.create(
        db=db,
        attributes=entity.model_dump(),
    )


@label_router.get("/", response_model=list[Label])
async def get_labels(
    q: GetLabelQueryParams = Depends(),
    db: Session = Depends(get_db),
) -> Any:
    """Get all labels."""
    return await label_controller.get_all(db=db, q=q)


@label_router.get("/{label_id}")
async def get_label(
    label_id: PositiveInt,
    db: Session = Depends(get_db),
) -> Label:
    """Get label by id."""
    return await label_controller.get_by_id(db=db, id_=label_id)


@label_router.post("/")
async def post_label(
    label: CreateLabel,
    db: Session = Depends(get_db),
) -> Label:
    """Create a new label."""
    return await label_controller.create(
        db=db,
        attributes=label.model_dump(),
    )
