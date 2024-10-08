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

ARG PORT=8000
EXPOSE ${PORT}

COPY pyproject.toml poetry.lock* ./

# Install project dependencies in virtual environment with poetry
ENV PATH="$APP_PATH/.venv/bin:$PATH"
RUN poetry config virtualenvs.in-project true --local \
    && python -m venv .venv \
    && poetry install --only main --no-root

# Copy source code and install main package
COPY alembic alembic
COPY . .
RUN poetry install --only main

CMD [ "/bin/sh", "entrypoint.sh" ]
