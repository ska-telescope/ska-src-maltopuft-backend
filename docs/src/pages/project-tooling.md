# Tooling

## Static code analysis

This project uses the following tools for static code analysis:

* [black](https://black.readthedocs.io/en/stable/) for code formatting
* [mypy](https://mypy.readthedocs.io/en/stable/) for static type checking.
* [flake8](https://flake8.pycqa.org/en/latest/) and [pylint](https://www.pylint.org/) lint rules.
* [isort](https://pycqa.github.io/isort/) import sorting rules.

With the exception of `mypy`, all of these tools are configured to run in the CI pipeline.

Before commiting any changes to the repository, you can run static code analysis locally with:

```bash
make pre-commit
```

### Optional

[Ruff](https://docs.astral.sh/ruff/) is also configured and can be used to replace most of the functionality of [isort](https://pycqa.github.io/isort/), [flake8](https://flake8.pycqa.org/en/latest/) and [pylint](https://pylint.pycqa.org/en/latest/index.html) within the project.

```bash
# Don't auto-fix issues
ruff check .

# Auto-fix issues
ruff check . --fix
```

The ruff linter can watch changes to a directory to alert you about lint rule violations on-the-fly:

```bash
ruff check . --watch
```

At this point in time, there are still some minor differences between `black` and `ruff-format`. Hence, it is not recommended to use the `ruff-format` with this repository.

## Tests

All unit and integration tests are defined in `./tests`. [PyTest](http://pythontesting.net/framework/pytest/pytest-introduction/) is used as the testing framework. Use the command below to run tests:

```bash
make python-test

### ----- OR ----- ###

python -m pytest .
```

Running the tests creates the `build` directory. The `html` test report can be viewed in any modern web browser by opening `./build/reports/code-coverage/index.html`. All the tests should pass before merging code.