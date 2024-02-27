FROM python:3.11-alpine

RUN apk update && apk add python3-dev gcc libc-dev git postgresql-client

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install gunicorn~=21.2
ADD src/requirements.txt /app/

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r /app/requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

ADD src /app
ADD deploy /conf

RUN chmod +x /conf/server-entrypoint.sh
RUN chmod +x /conf/worker-entrypoint.sh
