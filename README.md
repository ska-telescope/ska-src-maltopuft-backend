# ska-src-maltopuft-backend

## MALTOPUFT

MALTOPUFT is a prototype MAchine Learning TOolkit for PUlsars and Fast Transients.

The toolkit provides a unified interface to view single pulse candidates identified by SKA precursor telescopes (MeerTRAP) and assign "ground-truth" labels for use in Machine Learning classifier training.

This repository hosts code for the MALTOPUFT API web service. Please refer to the [MALTOPUFT API documentation](https://readthedocs.org/dashboard/) for more information.

MALTOPUFT is developed, maintained and tested by the UK SKA Regional Centre (UK SRC).

## Roadmap

In the future, the toolkit plans to support:

1. View and label periodic pulse (pulsar) data.
2. Retrieve and create version controlled datasets for use in the Machine Learning classifier training and evaluation pipelines.
3. View and label data from additional precursor telescopes and, once operational, the SKA.

## Contributing
### Clone the repository

The repository and all submodules can be cloned with:

```bash
git clone --recurse-submodules git@gitlab.com:ska-telescope/src/ska-src-maltopuft-backend.git
```

Changes to the remote repository and submodules can be pulled into the local copy with:

```bash
git fetch --all && git pull --recurse-submodules
```

## Documentation

Documentation is generated with [sphinx](https://www.sphinx-doc.org/en/master/). All configuration and documentation pages are stored in `./docs`.

### Build locally

To build the documentation, first ensure that `docs` dependencies are installed and use `make`:

```bash
make docs-build html

### ----- OR ----- ###

# Install doc dependencies
poetry install --with docs --no-root

# Build the docs
cd ./docs
make clean && make html
```

The docs are built in `./docs/build` and can be viewed in any modern web browser by opening `./docs/build/html/index.html`.

### Add new documentation

The documentation is configured to auto-generate docs for all functions, classes and class methods in the `./src` package.

General documentation pages should be created in `./docs/src/pages/*.rst`. These pages should be referenced in `./docs/src/index.rst` to be included in the built docs.

Also note that interactive [OpenAPI](https://www.openapis.org/) documentation can be viewed by navigating to the `/docs` endpoint.
