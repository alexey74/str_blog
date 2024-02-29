
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

gen_api_tests: blog/tests/integration/test_api_auto.py

blog/tests/integration/test_api_auto.py: blog/*.py
	python manage.py generate_viewset_tests -r blog.urls.router --variant pytest > $@


.PHONY: all test admuser run import flushdb clean
