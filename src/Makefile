
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com

-include .env
export

all: test run

test:
	pytest .

requirements.txt: ../.venv/**
	pip freeze > $@

admuser:
	python manage.py createsuperuser --noinput

run:
	python manage.py runserver 127.0.0.1:8888

import:
	python manage.py import_jph

flushdb:
	python manage.py sqlflush | python manage.py dbshell


.PHONY: all test admuser run import flushdb clean
