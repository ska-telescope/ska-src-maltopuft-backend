"""Create a FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from src.ska_src_maltopuft_backend.api import router


def init_routers(app_: FastAPI) -> None:
    """Include all routers defined in src.api initialisation."""
    app_.include_router(router)


def make_middleware() -> list[Middleware]:
    """Return an ordered list of "middleware" to be used by the Fast API application.

    Ordered means that earlier list elements take priority over later list elements.
    """
    return [
        Middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
    ]


def create_app() -> FastAPI:
    """Create a Fast API application."""
    app_ = FastAPI(middleware=make_middleware())
    init_routers(app_=app_)
    return app_


app = create_app()
