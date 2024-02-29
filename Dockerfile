FROM python:3.11-slim

# Poetry installation
ARG POETRY_HOME="/opt/poetry"
RUN apt update && \
    apt-get install -y curl && \
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

COPY main.py ./
COPY ./src ./src/

CMD [ "python", "./main.py" ]