# GNU makefile

test:
	$(MAKE) -C src $@ 

clean:
	rm -rf **/__pycache__/ **/.pytest_cache/ **/cov_html/ \
		**/cov.xml **/.coverage **/coverage.json **/*.py[co]

prune: clean
	rm -rf **/db.sqlite3 **/.venv/

.PHONY: clean prune
