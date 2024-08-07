"""Routers for KnownPulsar endpoints."""

import logging
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ska_src_maltopuft_backend.core.database.database import get_db
from ska_src_maltopuft_backend.core.factory import Factory

from .controller import KnownPulsarController
from .requests import GetKnownPulsarQueryParams
from .responses import KnownPulsar

logger = logging.getLogger(__name__)
catalogue_router = APIRouter()


@catalogue_router.get(
    "/pulsars",
    response_model=list[KnownPulsar],
)
async def get_known_pulsars(
    q: GetKnownPulsarQueryParams = Depends(),
    db: Session = Depends(get_db),
    pulsar_controller: KnownPulsarController = Depends(
        Factory().get_known_pulsar_controller,
    ),
) -> Any:
    """Retrieve known pulsars."""
    return await pulsar_controller.get_all(db=db, q=[q])
