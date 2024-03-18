# ska-src-maltopuft-backend

A prototype MAchine Learning TOolkit for PUlsars and Fast Transients (MALTOPUFT) backend.

## Prerequisites
### Container engine

* [Podman](https://podman.io/docs) is the preferred container engine, although [Docker](https://www.docker.com/get-started/) can be used equivalently (simply replace `podman` -> `docker` in commands). The steps outlined in this document assume that your container engine of choice is configured and running on your machine.
* [PostgreSQL database](https://www.postgresql.org/docs/16/index.html). The application is developed with the latest version at the time of writing (PostgreSQL 16.2) deployed on Alpine 3.19 OS.

## Build
### Local

It is recommended to deploy a local development environment with the provided [docker-compose.local.yaml](./docker/docker-compose.local.yaml) file.

```bash
podman compose -f "docker/docker-compose.local.yaml" down
podman compose -f "docker/docker-compose.local.yaml" up -d --build
```

Currently, this is only configured to bring up a development PostgreSQL database server (`maltopuftdb`) and perform periodic health checks with [pg_isready](https://www.postgresql.org/docs/current/app-pg-isready.html). The `maltopuftdb` container won't progress to 'healthy' status until the health check passes. However, to confirm this from the command line on your local machine run:

```bash
podman exec -it maltopuftdb pg_isready -U postgres
```

In the future, docker compose will bring up a full development environment for the backend application and all it's dependencies.