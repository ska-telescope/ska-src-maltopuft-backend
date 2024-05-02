"""Create a FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.ska_src_maltopuft_backend.api import router
from src.ska_src_maltopuft_backend.core.auth import BearerTokenAuthBackend
from src.ska_src_maltopuft_backend.core.config import settings


def init_routers(app_: FastAPI) -> None:
    """Include all routers defined in src.api initialisation."""
    app_.include_router(router)


def make_middleware() -> list[Middleware]:
    """Return an ordered list of "middleware" used by the Fast API
    application.

    Ordered means that earlier list elements take priority over later list
    elements.
    """
    return [
        Middleware(
            SessionMiddleware,
            secret_key=settings.MALTOPUFT_OIDC_AUTHORIZATION_STATE,
        ),
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=BearerTokenAuthBackend(),
        ),
    ]


def create_app() -> FastAPI:
    """Create a Fast API application."""
    app_ = FastAPI(middleware=make_middleware())
    init_routers(app_=app_)
    return app_


app = create_app()
