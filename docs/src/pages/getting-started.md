# Getting started

## Prerequisites

* Python >=3.11.
* [PostgreSQL database](https://www.postgresql.org/docs/16/index.html). The application is developed with the latest version at the time of writing (PostgreSQL 16.2) deployed on Alpine 3.19 OS.
* For containerised deployments, the only requirement is a working container engine installation running on your machine.
    * [Podman](https://podman.io/docs) is the preferred container engine. [Docker](https://www.docker.com/get-started/) can be used equivalently (as a first port of call, try simply replacing `podman --> docker` in any commands below).

## Run the application

After following one of the deployment methods below, navigating to `localhost:8000`, `127.0.0.1:8000` or `0.0.0.0:8000` in the browser should return the application landing page (`/`). API documentation generated with [OpenAPI](https://www.openapis.org/) can be viewed by navigating to the `/docs` endpoint.

### Compose (recommended)

It is recommended to deploy a local development environment with the provided `./docker/docker-compose.yaml` file. This method brings up all the application dependencies and configures the network connectivity between them on the local machine.

The build steps below build `Dockerfile`s on the local filesystem rather than using locally built images or pulling published images from a container registry. In order for the supplied `docker-compose.yaml` to work out-of-the-box, this repository (`ska-src-maltopuft-backend`) and the frontend repository (`ska-src-maltopuft-frontend`) must therefore exist at the same level in the directory tree, as shown below:

```bash
<parent-dir>
├─ ska-src-maltopuft-backend/
    ├─ docker/
        ├─ docker-compose.yaml
├─ ska-src-maltopuft-frontend/
```

Alternatively, the `build` fields in `docker-compose.yaml` can be modified to point to the respective directory.

Then, run the commands given below from the `ska-src-maltopuft-backend` directory to bring up the application development environment:


```bash
podman compose -f "docker/docker-compose.yaml" down
podman compose -f "docker/docker-compose.yaml" up -d --build
```

If you are only interested in bringing up the backend service and database, the second command given above can be modified to only bring up the required services:

```bash
podman compose  -f "docker/docker-compose.yaml" up -d --build maltopuftdb ska-src-maltopuft-backend
```

The `docker-compose.yaml` file is configured to first bring up a development PostgreSQL database server (`maltopuftdb`). After bringing up the database container, periodic health checks are performed with the [pg_isready](https://www.postgresql.org/docs/current/app-pg-isready.html) utility.

The `maltopuftdb` container won't progress to 'healthy' status until the database is ready to serve requests and the health check passes. The health check can be run equivalently from the command line on a local machine with the command below:

```bash
podman exec -it maltopuftdb pg_isready -U postgres
```

Once the database container is healthy a development backend web service (`ska-src-maltopuft-backend`) is then deployed. A basic health check is configured to retrieve a response from the `/ping` endpoint before the container progresses to the 'healthy' state.

Finally, once the backend container is healthy, the application frontend (`ska-src-maltopuft-frontend`) is initialised. A health check is configured to pass if the web page html is successfully retrieved with a HTTP GET request. The application frontend can be accessed by navigating to port `3000` in the browser.

After components are deployed and in a healthy state, the health checks continue to be issued every 30 seconds.

### Containerised

This method requires manual deployment of external application components (database, frontend) and network configuration between the application components.

```bash
podman build -t ska-src-maltopuft-backend:latest .
podman run -t -p 8000:8000/tcp ska-src-maltopuft-backend:latest
```

Note that the port specified in the above command (`8000`) is the same as the port exposed in `./Dockerfile`.

### Local

This method requires manual deployment of all application components and network configuration between them.

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
