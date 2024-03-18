# ska-src-maltopuft-backend

MALTOPUFT is a prototype MAchine Learning TOolkit for PUlsars and Fast Transients. The toolkit will provide a unified interface to:

1. View single pulse and periodic candidates identified by SKA precursors and, once operational, the SKA.
2. Assign "ground-truth" labels to candidates for use in Machine Learning classifier training.
3. Retrieve and create version controlled datasets for use in the Machine Learning classifier training and evaluation pipelines. 

This repository will hold all code relating to the MALTOPUFT backend web service.

## Run the application

### Local

The only requirement is a working Python 3.11 installation on the local machine.

```bash
# Install poetry
curl -sSL https://install.python-poetry.org | python3 -

# Create and activate a virtual environment with venv
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies in venv with poetry
poetry install --no-root

# Run the application
python main.py
```

Navigating to `0.0.0.0:8000` in the browser should return the application landing page (`/`).

### Containerised

* [Podman](https://podman.io/docs) is the preferred container engine, although [Docker](https://www.docker.com/get-started/) can be used equivilently (simply replace `podman` -> `docker` in the commands below). The steps below assume that your container engine of choice is configured and running on your machine:

```bash
podman build -t ska-src-maltopuft-backend:latest .
podman run -t -p 8000:8000/tcp ska-src-maltopuft-backend:latest
```

Navigating to `0.0.0.0:8000` in the browser should return the application landing page (`/`).

## Code formatting, linting and testing

* [Ruff](https://docs.astral.sh/ruff/) is used to replace most of the functionality of [black](https://black.readthedocs.io/en/stable/), [isort](https://pycqa.github.io/isort/), [flake8](https://flake8.pycqa.org/en/latest/) and [pylint](https://pylint.pycqa.org/en/latest/index.html). Use the command below to run the code formatter and linter:

```bash
ruff format . && ruff check . --fix
```

* All unit and integration tests are defined in [./tests](./tests). [PyTest](http://pythontesting.net/framework/pytest/pytest-introduction/) is used as the testing framework. Pytest is configured to run ruff's linter and perform static type checking with [mypy](https://www.mypy-lang.org/) while testing. Use the command below to run tests:

```bash
python -m pytest .
```

* Running the tests creates the `htmlcov` directory. The `html` test report can be viewed in any modern web browser by opening `./htmlcov/index.html`. All the tests should pass before merging code.

## Documentation

Documentation is generated with [sphinx](https://www.sphinx-doc.org/en/master/). All configuration and documentation pages are stored in `./docs`. To build the documentation, first ensure that `docs` dependencies are installed and use `make`:

```bash
# Install doc dependencies
poetry install --with docs --no-root

# Build the docs
cd ./docs
make clean && make html
```

The docs are built in `./docs/build` and can be viewed in any modern web browser by opening `./docs/build/html/index.html`. The documentation is configured to auto-generate docs for all functions, classes and class methods in the `./src` package. General documentation pages should be created in `./docs/src/package/*.rst`. These pages should be referenced in `./docs/src/index.rst` to be included in the built docs.
