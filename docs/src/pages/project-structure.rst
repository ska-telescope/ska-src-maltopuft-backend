Repository structure
====================

An outline of the repository structure is given below:

.. code-block:: console

    ska-src-maltopuft-backend/
    ├─ docs/
    ├─ src/
    │  ├─ app/
    │  │  ├─ api/
    │  │  ├─ models/
    │  ├─ candle/
    │  ├─ core/
    │  ├─ health/
    │  ├─ user/
    ├─ tests/
    ├─ main.py

.. note::
    The directory structure is subject to change during early prototyping. 

* `docs/`: User and developer documentation pages.
* `src/ska_src_maltopuft_backend/`: Application code.
    * `app/`: MALTOPUFT web-service initialisation.
        * `api/`: Defines versioned API "routers" which are the paths of REST endpoints exposed by the application.
        * `models/`: Central location for all MALTOPUFT database models.
    * `candle/`: Candidate handler feature.
    * `core/`: Generic application configuration and boilerplate code. For example modules that establish database connections, enforce Role-Based Access Control (RBAC) and define any base classes re-used by several application components will all be defined here.
    * `health/`: Health check feature.
    * `user/`: User feature.
* `tests`: Unit and integration tests.
* `main.py`: 
