.. _crud-docs:

===================================
Create, Read, Update, Delete (CRUD)
===================================

This documentation outlines the general structure used to implement Create, Read, Update and Delete (CRUD) operations in the application.

CRUD operations flow through the following application components:

1. Router
2. Controller
3. Repository

Router
======

When the application recieves a request, it first reaches the router layer. Please refer to the `FastAPI documentation <https://fastapi.tiangolo.com/>`_ for an excellent overview.

The router layer is reponsible for parsing incoming HTTP requests and routing them through the application via the appropriate data controllers based on the requester's permissions.

.. code-block:: python

    from fastapi import APIRouter, Depends

    router = APIRouter()


    @router.get("/")
    async def my_function(request: Request):
        if request.user.group == "GroupA":
            do_thing_A()
        elif request.user.group == "GroupB":
            do_thing_B()
        ...

Any user input data sent with the request is parsed and validated with `Pydantic <https://docs.pydantic.dev/latest/>`_ models.

.. code-block:: python

    from fastapi import APIRouter, Depends
    from pydantic import BaseModel

    router = APIRouter()


    class GetModelSchema(BaseModel):
        id: int
        name: str
        age: float

    class ReturnModelSchema(BaseModel):
        name: str


    @router.get("/", response_model=ReturnModelSchema) -> Any:
    async def my_function(data: GetModelSchema):
        return {"name": data.name}

.. tip::
    FastAPI serialises objects returned in routers to ``dict`` and then parses the response with ``ReturnModelSchema``. Therefore, it's preferable to return ``dict`` objects over ``Pydantic`` models in routers to ensure that objects aren't parsed and validated twice.

Controller
==========

The (data) controller layer applies the application-specific logic or manipulation required before the CRUD operation can be carried out.

A data controller base class is implemented in ``BaseController``. A model-specific data controller class (which inherits from the ``BaseController``) should be created for each type of model in the application:

.. code-block:: python

    from ska_src_maltopuft_backend.core.controller import BaseController

    from .models import MyThing
    from .repository import MyRepository
    from .requests import CreateMyThing, UpdateMyThing


    class MyController(BaseController[MyThing, CreateMyThing, UpdateMyThing]):
        def __init__(self, repository: MyRepository) -> None:
            super().__init__(
                model=MyThing,
                repository=repository,
            )
            self.repository = repository

In the example above, ``CreateMyThing`` (``UpdateMyThing``) can be either Pydantic models with the create (update) request schemas or ``None``. In the case where ``None`` is passed, then any create or update requests will raise a ``NotImplementedError``.

Controllers are instantiated with the required dependencies by ``Factory`` class methods. These class methods can then be dependency injected into the routers as shown below.

.. code-block:: python

    from fastapi import APIRouter, Depends

    from ska_src_maltopuft_backend.core.factory import Factory

    from .controller import MyController

    router = APIRouter()


    @router.get("/")
    async def test_my_controller(
        my_controller: MyController = Depends(
            Factory().get_my_controller,
        ),
    ):
        return await my_controller.get_all()

A controller may have a dependency one or more other controllers. In this case, the controller class's ``__init__`` method can be extended to include the dependent controller and the dependency can be configured in the ``Factory`` class method.

.. code-block:: python

    class MyController(BaseController[MyThing, CreateMyThing, UpdateMyThing]):
        def __init__(
            self,
            repository: MyRepository,
            dependent_controller: MyDependentController,
        ) -> None:
            super().__init__(
                model=MyThing,
                repository=repository,
                dependent_controller=dependent_controller,
            )
            self.repository = repository
            self.dependent_controller = dependent_controller

    class Factory:
        my_repository = partial(repositories.MyRepository, models.MyThing)

        def get_my_controller(self) -> controllers.MyController:
            return controllers.MyController(
                repository=self.my_repository(),
                dependent_controller=self.get_my_dependent_controller(),
            )

Repository
==========

Repositories are responsible for handling interactions with the database.

CRUD operations typically involve the application issuing SQL queries to the database to perform an operation (such as ``GET``) on the requested resource (such as ``users``).

To facilitate these operations, several core building blocks of SQL query statements (such as ``SELECT``, ``JOIN``, ``ORDER BY``, ``DELETE`` etc.) are implemented for an abstract SQLAlchemy model type (``ModelT``) in a repository base class (``BaseRepository``). The ``BaseRepository`` implements the SQL building blocks with the SQLAlchemy ORM:

.. code-block:: python

    from ska_src_maltopuft_backend.core.database.base import Base

    ModelT = TypeVar("ModelT", bound=Base)

    class BaseRepository(Generic[ModelT]):
        ...

As with the controllers, a model-specific repository class should be created for each type of model in the application and dependency injected in the controller ``Factory``.

.. code-block:: python

    from typing import TypeVar

    from ska_src_maltopuft_backend.core.repository import BaseRepository

    from .models import MyThing

    class MyRepository(BaseRepository[MyThing]):
        ...
