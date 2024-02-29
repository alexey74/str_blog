# GNU makefile
DOCKER_COMPOSE ?= docker-compose
COMPOSE_PROJECT_NAME ?= blog

-include .env
export

all: | dc-down build dc-up

lint:
	pre-commit run --all-files

test:
	$(MAKE) -C src $@ 

# Run tests inside a container stack
test-live:
	make dc-run args='--entrypoint /bin/sh server -c pytest'

clean:
	rm -rf **/__pycache__/ **/.pytest_cache/ **/cov_html/ \
		**/cov.xml **/.coverage **/coverage.json **/*.py[co]

prune: clean
	rm -rf **/db.sqlite3 **/.venv/

# Run a docker-compose command with optional arguments
dc-%:
	$(DOCKER_COMPOSE) -f deploy/docker-compose.yml $* $(args)

bg: 
	$(MAKE) dc-up args=-d

build: | src/requirements.txt dc-build


rebuild: src/requirements.txt
	$(MAKE) dc-build args=--no-cache

cmd:
	make dc-run args='--entrypoint /app/manage.py server $(cmd)'

sh:
	make dc-run args='--entrypoint /bin/sh server'

import:
	make cmd cmd='import_iph'

.PHONY: all test clean prune bg build rebuild sh cmd import
