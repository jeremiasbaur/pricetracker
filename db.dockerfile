FROM postgres:11.1-alpine

COPY ./DatabaseDumps/pricetracker_database.sql /docker-entrypoint-initdb.d/pricetracker_database.sql
#COPY ./db_init.sh /docker-entrypoint-initdb.d/db_init.sh

RUN mkdir /data
ENV PGDATA=/data
