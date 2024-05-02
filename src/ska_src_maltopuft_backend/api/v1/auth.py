"""Routers for OIDC login endpoints."""

import logging
import secrets

from fastapi import APIRouter, Request

from src.ska_src_maltopuft_backend.app.schemas.responses.auth import (
    LoginRedirect,
)
from src.ska_src_maltopuft_backend.core.config import settings

logger = logging.getLogger(__name__)
auth_router = APIRouter()


@auth_router.get("/login", response_model=LoginRedirect)
async def login(request: Request, redirect_uri: str) -> dict:
    """Re-direct user to login securely via SKA IAM."""
    # Generate state and store it in browser session
    state = secrets.token_urlsafe(30)
    request.session["state"] = state

    auth_url = (
        f"https://ska-iam.stfc.ac.uk/authorize"
        f"?response_type=code"
        f"&client_id={settings.MALTOPUFT_OIDC_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={settings.MALTOPUFT_OIDC_CLIENT_SCOPE}"
        f"&state={state}"
    )
    return {"login_url": auth_url}
