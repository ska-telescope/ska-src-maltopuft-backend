"""Create a FastAPI application."""

from fastapi import FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.authentication import AuthenticationMiddleware

from src.ska_src_maltopuft_backend.app.api import router
from src.ska_src_maltopuft_backend.core.auth import BearerTokenAuthBackend
from src.ska_src_maltopuft_backend.core.exceptions import MaltopuftError


def init_routers(app_: FastAPI) -> None:
    """Include all routers defined in src.api initialisation."""
    app_.include_router(router)


def init_listeners(app_: FastAPI) -> None:
    """Register Fast API app listeners."""

    @app_.exception_handler(MaltopuftError)
    async def custom_exception_handler(
        request: Request,  # pylint: disable=W0613 # noqa: ARG001
        exc: MaltopuftError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": exc.message,
                "status_code": exc.status_code,
            },
        )


def make_middleware() -> list[Middleware]:
    """Return an ordered list of "middleware" used by the Fast API
    application.

    Ordered means that earlier list elements take priority over later list
    elements.
    """
    return [
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
            on_error=BearerTokenAuthBackend.on_auth_error,
        ),
    ]


def create_app() -> FastAPI:
    """Create a Fast API application."""
    app_ = FastAPI(middleware=make_middleware())
    init_routers(app_=app_)
    init_listeners(app_=app_)
    return app_


app = create_app()
