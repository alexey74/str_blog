test:
	pytest .

requirements.txt:
	pip freeze > $@

admuser:
	python manage.py createsuperuser --username admin --email admin@example.com

run:
	python manage.py runserver

import:
	python manage.py import_jph

flushdb:
	python manage.py sqlflush | python manage.py dbshell
