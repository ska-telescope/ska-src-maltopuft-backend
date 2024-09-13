.. _auth-docs:

================================
Authentication and Authorization
================================

This documentation outlines the authentication and authorization process in the MALTOPUFT application.

.. tip::
    Authentication can be toggled on/off with the `AUTH_ENABLED` environment variable. Authentication is enabled by default and can be disabled by setting `AUTH_ENABLED` to 0. 

Introduction
============

Authentication
--------------

Navigating to the MALTOPUFT frontend in the web browser and clicking the `Login` button starts the login flow.

The login flow calls the SKA auth-api `/login` endpoint, which redirects the user to login securely via `SKA IAM <https://ska-iam.stfc.skao>`_. Logging in via SKA-IAM redirects the user to the `/callback` route on the MALTOPUFT frontend, where the `OIDC PKCE flow <https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow-with-pkce>`_ begins.

After verifying the login, a `JWT <https://auth0.com/learn/json-web-tokens#!>`_ (referred to as the 'token') is returned and stored in the user's browser local storage. The token is embedded in the Authorization header of every HTTP request sent to the backend service.

Authorization
-------------

When an HTTP request reaches the MALTOPUFT backend, a series of auth operations are performed. The token extracted from the request headers is sent to the SKA auth-api `/token/exchange/maltopuft-api` endpoint.

At a high-level, this endpoint:

1. Verifies the authenticity of the token sent in the request
2. Exchanges the token for a maltopuft-api access token

.. note::
    
    Users must be a member of the `services/maltopuft-api` group in order to retrieve an exchanged token from the SKA IAM auth-api at step 2 above.

The MALTOPUFT backend injects user identity and permissions into the request, which can be accessed throughout the application.

Using auth in the application
=============================

The code sample below provides a minimal working example for using auth in MALTOPUFT.

.. code-block:: python

    from fastapi import APIRouter, Depends
    from ska_src_maltopuft_backend.core.auth import (
        Authenticated,
        AuthorizationChecker,
        UserGroups,
    )

    router = APIRouter()


    @router.get("/unprotected")
    async def unprotected_route() -> None:
        return "Anyone can access this route."

    @router.get("/authenticated", Depends(Authenticated))
    async def authenticated_route() -> None:
        return "All authenticated users can access this route, no matter which security groups they are a member of."

    @router.get("/user-only", Depends(AuthorizationChecker([UserGroups.MALTOPUFT_USER])))
    async def authenticated_route() -> None:
        return "Only users who are members of the `src/maltopuft/user` group can access this route."
