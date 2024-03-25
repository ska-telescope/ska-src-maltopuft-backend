# Tooling

## Code formatting and linting

[Ruff](https://docs.astral.sh/ruff/) is used to replace most of the functionality of [black](https://black.readthedocs.io/en/stable/), [isort](https://pycqa.github.io/isort/), [flake8](https://flake8.pycqa.org/en/latest/) and [pylint](https://pylint.pycqa.org/en/latest/index.html). Use the command below to run the code formatter and linter:

```bash
# Don't auto-fix issues
ruff format . --diff && ruff check .

# Auto-fix issues
ruff format . && ruff check . --fix
```

## Tests

All unit and integration tests are defined in `./tests`. [PyTest](http://pythontesting.net/framework/pytest/pytest-introduction/) is used as the testing framework. Pytest is configured to run ruff's linter and perform static type checking with [mypy](https://www.mypy-lang.org/) while testing. Use the command below to run tests:

```bash
python -m pytest .
```

Running the tests creates the `htmlcov` directory. The `html` test report can be viewed in any modern web browser by opening `./htmlcov/index.html`. All the tests should pass before merging code.