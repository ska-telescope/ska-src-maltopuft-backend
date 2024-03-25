# Getting started

## Clone the repository

```bash
git@gitlab.com:ska-telescope/src/ska-src-maltopuft-backend.git
cd ska-src-maltopuft-backend
```

## Run the application

After following one of the deployment methods below, navigating to `localhost:8000`, `127.0.0.1:8000` or `0.0.0.0:8000` in the browser should return the application landing page (`/`). API documentation generated with [OpenAPI](https://www.openapis.org/) can be viewed by navigating to `127.0.0.1:8000/docs`.

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

### Containerised

[Podman](https://podman.io/docs) is the preferred container engine, although [Docker](https://www.docker.com/get-started/) can be used equivilently (simply replace `podman` -> `docker` in the commands below). The steps below assume that your container engine of choice is configured and running on your machine:

```bash
podman build -t ska-src-maltopuft-backend:latest .
podman run -t -p 8000:8000/tcp ska-src-maltopuft-backend:latest
```