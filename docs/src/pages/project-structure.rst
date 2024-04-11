Repository structure
====================

An outline of the repository structure is given below:

.. code-block:: console

    ska-src-maltopuft-backend/
    ├─ docs/
    ├─ src/
    │  ├─ api/
    │  │  ├─ v1/
    │  ├─ app/
    │  │  ├─ models/
    │  │  ├─ schemas/
    │  │  │  ├─ requests/
    │  │  │  ├─ responses/
    │  ├─ core/
    │  │  ├─ config.py
    │  │  ├─ database.py
    │  │  ├─ server.py
    ├─ tests/
    ├─ main.py

.. note::
    The directory structure is subject to change during early prototyping. 

* `docs`: Developer documentation pages.
* `src.ska_src_maltopuft_backend`: Application code.
    * `api`: Defines versioned API "routers" which are the paths of REST endpoints exposed by the application.
    * `app`: Application-specific logic.
        * `models`: SQLAlchemy models.
        * `schemas`: Schemas for application requests and responses.
    * `core`: Generic application configuration and boilerplate code. For example modules that establish database connections, enforce Role-Based Access Control (RBAC) and define any base classes re-used by several application components will all be defined here.
        * `config`: Application configuration.
        * `database`: Database connection.
        * `server`: Creates a FastAPI application.
* `tests`: Unit and integration tests.
