Repository structure
====================

An outline of the repository structure is given below:

.. code-block:: console

    ska-src-maltopuft-backend/
    ├─ docs/
    ├─ src/
    │  ├─ ska-src-maltopuft-backend/
    │  │  ├─ app/
    │  │  │  ├─ api/
    │  │  │  ├─ models/
    │  │  │  ├─ schemas/
    │  │  ├─ candle/
    │  │  ├─ core/
    │  │  ├─ health/
    │  │  ├─ label/
    │  │  ├─ user/
    │  │  ├─ main.py
    ├─ tests/
    ├─ entrypoint.sh

.. note::
    The directory structure is subject to change during early prototyping. 

* `docs/`: User and developer documentation pages.
* `src/ska_src_maltopuft_backend/`: Application code.
    * `app/`: MALTOPUFT web-service initialisation.
        * `api/`: Defines versioned API "routers" which are the paths of REST endpoints exposed by the application.
        * `models/`: Central location for all MALTOPUFT database models.
        * `schemas/`: Central location for all MALTOPUFT API request/response data models.
    * `candle/`: Candidate handler feature for processing single pulse and periodic candidates.
    * `core/`: Generic application configuration and boilerplate code. For example modules that establish database connections, enforce Role-Based Access Control (RBAC) and define any base classes re-used by several application components will all be defined here.
    * `health/`: Health check feature.
    * `label/`: Candidate labelling feature.
    * `user/`: User feature.
    * `main.py`: The FastAPI application entrypoint.
* `tests`: Unit and integration tests.
* `entrypoint.sh`: The Dockerfile entrypoint shell script. Runs database migrations and starts the FastAPI application.

