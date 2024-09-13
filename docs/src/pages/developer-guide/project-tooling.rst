=======
Tooling
=======

This documentation outlines the differnt tooling used in the project.

Before commiting any changes to the repository, static code analysis and tests can be run locally with:

.. code-block:: bash

    make pre-commit

Static code analysis
====================

The project uses the following tools for static code analysis:

* `black <https://black.readthedocs.io/en/stable/>`_ for code formatting
* `mypy <https://mypy.readthedocs.io/en/stable/>`_ for static type checking.
* `flake8 <https://flake8.pycqa.org/en/latest/>`_ and `pylint <https://www.pylint.org/>`_ lint rules.
* `isort <https://pycqa.github.io/isort/>`_ import sorting rules.

With the exception of ``mypy``, all of these tools are configured to run in the CI pipeline.

The rules and configuration options for the tools are found in ``pyproject.toml``.

Optional
--------

`Ruff <https://docs.astral.sh/ruff/>`_ is also configured and can be used to replace most of the functionality of ``isort``, ``flake`` and ``pylint`` within the project.

.. code-block:: bash

    # Don't auto-fix issues
    ruff check .

    # Auto-fix issues
    ruff check . --fix

The ``ruff`` linter can watch changes to a directory to alert you about lint rule violations on-the-fly:

.. code-block:: bash

    ruff check . --watch

At this point in time, there are still some minor differences between ``black`` and ``ruff-format``. Therefore it's not currently recommended to replace ``black`` with ``ruff-format``.

Tests
=====

All unit and integration tests are defined in the ``./tests`` directory with the `PyTest <http://pythontesting.net/framework/pytest/pytest-introduction/>`_ test framework.

MALTOPUFT API implements behaviour-driven tests using the `Gherkin <https://docs.cucumber.io/docs/gherkin/reference/>`_ syntax with the `pytest-bdd <https://pytest-bdd.readthedocs.io/en/stable/>`_ plugin.

Tests can be run in the following ways:

.. code-block:: bash

    make python-test

    ### ----- OR ----- ###

    python -m pytest .

In addition to the test summary being output to stdout, running the tests creates a ``./build`` directory containing an HTML test report. The test report can be viewed in any modern web browser by opening ``./build/reports/code-coverage/index.html``, although this feature is of most use in the CI pipeline.

.. note::

    All tests should pass before merging code, unless there is an exceptional reason why they are expected to fail.

    In this case, tests can be skipped (`pytest.mark.skip("skip reason") <https://docs.pytest.org/en/6.2.x/skipping.html#skipping-test-functions>`_) or marked as an expected failure (`pytest.mark.xfail() <https://docs.pytest.org/en/6.2.x/skipping.html#xfail-mark-test-functions-as-expected-to-fail>`_).

    BDD tests can be skipped by tagging the scenario with the ``@skip`` tag.

    If any of these options are used, please raise a Jira ticket outlining any follow-up work required.

.. warning::

    If the database is deployed with docker, then you must ensure that the database is visible to the host where the test command is being executed.

    For example, if both the application and database are deployed in the same container network (e.g. after deploying with ``compose``) then this can be achieved by executing test commands *inside* the backend application container (i.e. running ``docker exec -it ska-src-maltopuft-backend make python-test``) or by updating the ``MALTOPUFT_DB_HOST`` environment variable to point to the IP address of the docker container, etc.
