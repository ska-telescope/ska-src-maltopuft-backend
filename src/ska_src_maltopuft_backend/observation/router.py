"""Routers for Candidate Handler endpoints."""

import logging
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ska_src_maltopuft_backend.core.database.database import get_db
from ska_src_maltopuft_backend.core.factory import Factory

from .controller import ObservationController
from .requests import GetObservationQueryParams
from .responses import Observation

logger = logging.getLogger(__name__)
observation_router = APIRouter()


@observation_router.get(
    "/",
    response_model=list[Observation],
)
async def get_observations(
    q: GetObservationQueryParams = Depends(),
    db: Session = Depends(get_db),
    observation_controller: ObservationController = Depends(
        Factory().get_observation_controller,
    ),
) -> Any:
    """Get observations in by descending t_min (start time)."""
    return await observation_controller.get_all(
        db=db,
        order_={"desc": ["t_min"]},
        q=[q],
    )
