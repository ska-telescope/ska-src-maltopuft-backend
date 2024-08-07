"""Initialise all API v1 routers."""

from fastapi import APIRouter

from ska_src_maltopuft_backend.app.api.responses import api_responses
from ska_src_maltopuft_backend.candle.router import candle_router
from ska_src_maltopuft_backend.catalogue.router import catalogue_router
from ska_src_maltopuft_backend.health.router import health_router
from ska_src_maltopuft_backend.label.router import label_router
from ska_src_maltopuft_backend.observation.router import observation_router
from ska_src_maltopuft_backend.user.router import user_router

v1_router = APIRouter()

v1_router.include_router(
    health_router,
    tags=["Health check"],
    responses={
        404: {"description": "Not found."},
    },
)
v1_router.include_router(
    user_router,
    prefix="/users",
    tags=["User"],
    responses=api_responses,  # type: ignore[arg-type]
)
v1_router.include_router(
    candle_router,
    prefix="/candle",
    tags=["Candidate Handler"],
    responses=api_responses,  # type: ignore[arg-type]
)
v1_router.include_router(
    label_router,
    prefix="/labels",
    tags=["Label"],
    responses=api_responses,  # type: ignore[arg-type]
)
v1_router.include_router(
    observation_router,
    prefix="/obs",
    tags=["Observation"],
    responses=api_responses,  # type: ignore[arg-type]
)
v1_router.include_router(
    catalogue_router,
    prefix="/catalogues",
    tags=["Catalogues"],
    responses=api_responses,  # type: ignore[arg-type]
)
