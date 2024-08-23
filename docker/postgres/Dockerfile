FROM postgres:16.3

RUN apt update -y && \
    apt install -y cmake \
    postgresql-server-dev-16 \
    postgresql-16-pgsphere

COPY ./initdb-pgsphere.sh /docker-entrypoint-initdb.d/
