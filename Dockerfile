FROM python:3.11-slim

ARG POETRY_HOME="/opt/poetry"

# Install poetry and any other binaries required.
# libpq-dev and gcc binaries are required to use the psycopg python
# package which handles connections to a PostgreSQL database.
RUN apt update && \
    apt-get install -y curl libpq-dev gcc make && \
    curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python3 - && \
    ln -s ${POETRY_HOME}/bin/poetry /usr/local/bin/poetry

ARG APP_PATH=/ska-src-maltopuft-backend
WORKDIR ${APP_PATH}

# Copy poetry.lock* in case it doesn't exist in the repo
COPY pyproject.toml poetry.lock* ./

# Create virtual environment and install runtime dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-root

ARG PORT=8000
EXPOSE ${PORT}

COPY alembic.ini ./alembic.ini
COPY main.py ./
COPY entrypoint.sh ./
COPY alembic ./alembic
COPY ./src ./src/

CMD [ "/bin/sh", "entrypoint.sh" ]
