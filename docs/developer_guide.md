# Developer Guide

## Overview

The code is based on Python version 3.11 though it should work on any version higher that 3.8.
The project is designed for development in a virtual environment.
The requirements file is currently static and monolithic.

In order to initialize the environment, run:

```sh
    python -m venv .venv
    . .venv/bin/activate
    python -m pip install -r src/requirements.txt
    make run
```

This will bring up a development server on top of a SQLite database on port 8000 on local host.

## Linting

Linting is provided by MegaLinter via a `pre-commit` hook.

In order to check the whole codebase locally, run `make lint`.

## Testing

Tests are based on `pytest` framework.
In order to run all basic tests locally, run `make test` or just `pytest src/`
This will execute pytest with a SQLite database and skip some tests due to its limitations.

In order to run advanced tests (namely, API compliance checks based on `schemathesis`),
the tests must be run on a Postgres database.
Run `make test-live` to start such tests inside a local container stack.

## Automatic Documentation

The project uses MkDocs with `mkdocstrings` extension in order to generate the documentation
automatically out of static Markdown files and inline documentation contained in the codebase.
The default docstring format is Google.

In order to rebuild the documentation and start a local documentation server, run `mkdocs serve`
