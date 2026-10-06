FROM postgres:16-alpine

COPY ./init.sql /docker-entrypoint-initdb.d/
COPY ./tags.sql /docker-entrypoint-initdb.d/

