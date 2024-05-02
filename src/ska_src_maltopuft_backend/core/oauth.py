"""MALTOPUFT backend OAuth client instance."""

from authlib.integrations.starlette_client import OAuth

from src.ska_src_maltopuft_backend.core.config import settings

oauth = OAuth()
oauth.register(
    name="ska_iam",
    server_metadata_url=settings.MALTOPUFT_OIDC_SERVER,
    client_id=settings.MALTOPUFT_OIDC_CLIENT_ID,
    client_secret=settings.MALTOPUFT_OIDC_CLIENT_SECRET,
    client_kwargs={"scope": settings.MALTOPUFT_OIDC_CLIENT_SCOPE},
    authorize_state=settings.MALTOPUFT_OIDC_AUTHORIZATION_STATE,
)
