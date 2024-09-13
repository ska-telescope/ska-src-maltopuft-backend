=========
MALTOPUFT
=========

MALTOPUFT is a prototype MAchine Learning TOolkit for PUlsars and Fast Transients.

The toolkit provides a unified interface to view single pulse candidates identified by SKA precursor telescopes (MeerTRAP) and assign "ground-truth" labels for use in Machine Learning classifier training.

MALTOPUFT does this by providing a database server for storing pulsar and fast-transient candidate (meta) data and a `RESTful (REST) API <https://aws.amazon.com/what-is/restful-api/>`_ which allows clients to interact with candidates stored in the database. MALTOPUFT's frontend component provides a GUI to interactively view and label candidates with the REST API.

.. tip::

    REST APIs provide a unified interface for clients to interact with resources stored on remote servers (often a database) over a network.

    In general, a client can be any entity that requests resources from the server. Clients often make JSON formatted requests via HTTP.

    REST APIs expose several *paths* or *endpoints* to clients which the server uses to identify the intended resource. HTTP methods (such as `GET`, `POST`, `PUT`, `DELETE`) are used to specify what the server needs to do to the resource.

Components
==========

---------------
Database server
---------------

The MALTOPUFT API primarily requests resources from a database server (``maltopuftdb``). ``maltopuftdb`` is a PostgreSQL Relational Database Management System (RDBMS).

-----------------------
MALTOPFUT API (backend)
-----------------------

A REST API web service built with the `FastAPI <https://fastapi.tiangolo.com/>`_ web framework.

This repository holds all code relating to the MALTOPUFT RESTful API web service.

The backend service is responsible for initialising database connections. Create, Read, Update and Delete (CRUD) operations against the database are handled with the `SQLAlchemy <https://www.sqlalchemy.org/>`_ library. SQLAlchemy is an object-relational mapping (ORM) library which provides a convenient way to express database models and queries in application code.

--------------------------------------------
Candidate viewer and labeller GUI (frontend)
--------------------------------------------

The frontend component provides a GUI for viewing and labelling single pulse and periodic candidates. The GUI component will often be referred to as the "frontend". Please refer to `ska-src-maltopuft-frontend <https://gitlab.com/ska-telescope/src/ska-src-maltopuft-frontend>`_ for more information.

--------------------------------
Authentication and authorization
--------------------------------

Authentication and authorisation are often referred to "auth".

Authentication essentially asks the question "*is this user who they say they are?*". If the answer is "*yes*", then authorisation goes on to ask "*does this user have permission to perform the requested operation on the specified resource(s)?*".

MALTOPUFT uses an `SKA IAM <https://ska-iam.stfc.ac.uk/login>`_ Open ID Connect (OIDC) client and the `ska-src-auth-api <https://gitlab.com/ska-telescope/src/src-service-apis/ska-src-auth-api/-/tree/main?ref_type=heads>`_ to handle auth.

Please refer to the `(external) How OIDC works <https://openid.net/developers/how-connect-works/>`_ documentation for an overview.

Architecture overview
=====================

At a high level, the components outlined in the previous section interact in the following ways:

.. figure:: ../../images/architecture-diagram.png
   :align: center

   MALTOPUFT web service architecture.

