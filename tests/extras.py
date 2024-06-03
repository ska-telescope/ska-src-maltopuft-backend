"""Mock starlette request interface."""

from typing import Any

from starlette.authentication import AuthCredentials, BaseUser
from starlette.datastructures import Headers
from starlette.requests import Request


def build_request(  # noqa: PLR0913
    method: str = "GET",
    server: str = "http://localhost:8000",
    path: str = "/",
    headers: dict[str, Any] | None = None,
    user: BaseUser | None = None,
    auth: AuthCredentials | None = None,
) -> Request:
    """Builds a mock starlette request for use in testing."""
    if headers is None:
        headers = {}

    return Request(
        {
            "type": "http",
            "path": path,
            "headers": Headers(headers).raw,
            "http_version": "1.1",
            "method": method,
            "scheme": "https",
            "client": ("127.0.0.1", 8000),
            "server": (server, 80),
            "user": user,
            "auth": auth,
        },
    )
