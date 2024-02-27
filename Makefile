# GNU makefile
DOCKER_COMPOSE ?= docker-compose
COMPOSE_PROJECT_NAME ?= blog

-include .env
export
test:
	$(MAKE) -C src $@ 

clean:
	rm -rf **/__pycache__/ **/.pytest_cache/ **/cov_html/ \
		**/cov.xml **/.coverage **/coverage.json **/*.py[co]

prune: clean
	rm -rf **/db.sqlite3 **/.venv/

dc-%:
	$(DOCKER_COMPOSE) -f deploy/docker-compose.yml $* $(args)

.PHONY: test clean prune
