FROM python:3.11-alpine

RUN apk update && apk add --no-cache python3-dev gcc libc-dev git postgresql-client

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir gunicorn~=21.2
COPY src/requirements.txt /app/

# see https://stackoverflow.com/questions/46711990/error-pg-config-executable-not-found-when-installing-psycopg2-on-alpine-in-dock
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r /app/requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY src /app
COPY deploy /conf

RUN chmod +x /conf/*-entrypoint.sh
