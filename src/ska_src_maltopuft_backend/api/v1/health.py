"""Routers for health check endpoints."""

import fastapi
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.ska_src_maltopuft_backend.app.schemas.responses.health import (
    Status,
    StatusEnum,
)
from src.ska_src_maltopuft_backend.core.config import settings
from src.ska_src_maltopuft_backend.core.database import (
    get_db,
    ping_db_from_pool,
)
from src.ska_src_maltopuft_backend.core.dependencies.authorization import (
    AuthorizationChecker,
)
from src.ska_src_maltopuft_backend.core.schemas import UserGroups

health_router = APIRouter()


@health_router.get("/ping")
async def ping() -> Response:
    """Return an empty 'ok' response to clients.

    Returns HTTP status code:
        HTTP_204_NO_CONTENT if no issues were encountered.
        HTTP_404_NOT_FOUND if the application is offline.
        HTTP_500_INTERNAL_SERVER_ERROR otherwise.
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@health_router.get("/health/app")
async def health_app() -> Status:
    """Return a 'HEALTHY' response to clients if the service is available.

    Returns HTTP status code:
        HTTP_204_NO_CONTENT if no issues were encountered.
        HTTP_404_NOT_FOUND if the application is offline.
        HTTP_500_INTERNAL_SERVER_ERROR otherwise.
    """
    return Status(name=settings.APP_NAME, status=StatusEnum.HEALTHY)


@health_router.get(
    "/health/db",
    dependencies=[
        Depends(AuthorizationChecker([UserGroups.MALTOPUFT_ADMIN])),
    ],
)
async def health_db(db: Session = Depends(get_db)) -> Status:
    """Return a 'HEALTHY' response to clients if the database is available.

    Note that, unlike health check requests for the application itself, an
    "UNAVAILABLE" response from the database will still return a HTTP_200_OK
    response code to the client.
    """
    try:
        ping_db_from_pool(db=db)
        db_status = StatusEnum.HEALTHY
    except fastapi.HTTPException:
        db_status = StatusEnum.UNAVAILABLE

    return Status(
        name=settings.MALTOPUFT_POSTGRES_HOST,
        status=db_status,
    )
