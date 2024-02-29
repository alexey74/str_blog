# Architecture

## Overview

The project is based on Django with Django REST Framework as the API platform.

Background tasks execution (such as replication/push to JSON Placeholder API) is handled by Celery with celery-beat
extension providing database-backed periodic tasks.

OpenAPI-compliant API schema is generated using `drf_yasg` which also provides Swagger and Redoc UI for API inspection in browsers.

Communication with external API (JSON Placeholder demo API) is handled by the `apiclient` package.

## Deployment

The project is packaged as a Docker compose stack, with main Django web server, Celery beat process, worker and Flower monitoring portal
based on the same Docker image defined by a Dockerfile.

The stack uses `nginx` as a reverse proxy and static files server.

Caching and task queue brokerage is implemented on Redis platform.

Production database is based on PostgreSQL.

The stack exposes post 8000 for the main web server and port 5555 for the Flower monitor.

## CI/CD

CI/CD is based on GitHub workflow actions, with an automatic run of linters, basic tests, and documentation generation.
The documentation generation system is based on MkDocs with `mkdocstrings` extension and will deploy results to GitHub pages.
