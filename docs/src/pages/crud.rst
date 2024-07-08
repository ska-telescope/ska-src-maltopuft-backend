.. _crud-docs:

====
CRUD
====

This documentation outlines the general structure used to implement Create, Read, Update and Delete (CRUD) operations in the application.

The flow of CRUD operations can be broken down into the following layers or components:

1. Router
2. Controller
3. Repository

Router
======

When the applicaiton recieves a request, it first reaches the router layer.

The router layer is reponsible for parsing incoming HTTP requests and routing them through the application via the correct data controllers based on the requester's permissions.

Controller
==========

The (data) controller layer is responsible for using one or more components from the model repository, in combination with any application-specific logic or manipulation required, to fulfil a request.

A data controller abstraction is implemented in `BaseController`. A model-specific instance of data controller should be created for each type of model in the application.

Repository
==========

The repository is responsible for handling interactions with the persistence layer (database).

CRUD operations typically involve the application issuing SQL queries to the database to perform an operation (such as `GET`) on the requested resource (such as `users`).

To facilitate these operations, several core building blocks of SQL query statements (such as `SELECT`, `JOIN`, `ORDER BY`, `DELETE` etc.) a persistence abstraction (`BaseRepository`) is implemented for an abstract SQLAlchemy model with the SQLAlchemy ORM.

A model-specific instance of the persistence abstraction should be created for each type of model in the application.
