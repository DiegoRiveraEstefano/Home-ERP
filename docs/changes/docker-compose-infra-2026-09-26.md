# Docker Infrastructure and Compose Setup (2026-09-26)

## Summary of Changes
- Created Docker configurations under `compose/`:
  - `compose/django/Dockerfile`: Multi-stage build with `uv:python3.14-bookworm-slim` and `python:3.14-slim`, non-root user `home_erp`.
  - `compose/django/entrypoint.sh`: POSIX/bash strict mode container entrypoint.
  - `compose/postgresql/postgresql.conf`: OLTP configuration for PostgreSQL 15/17.
  - `compose/redis/redis.conf`: Redis caching and Celery broker configuration.
  - `compose/seaweedfs/s3.json`: S3 credentials and identities configuration.
  - `compose/nginx/Dockerfile` and `compose/nginx/nginx.conf`: Nginx reverse proxy with gzip and static/media handling.
  - `compose/docs/Dockerfile`: Sphinx live-reloading documentation server.
- Created and configured Docker Compose files:
  - `docker-compose.local.yml`: Exposes PostgreSQL (5432), Redis (6379), and SeaweedFS (8333, 8888, 9333) for local host development.
  - `docker-compose.staging.yml`: Staging stack with PostgreSQL, Redis, SeaweedFS, Granian Web, Celery workers (default, io_heavy, cpu_heavy), Celery Beat, and Nginx.
  - `docker-compose.prod.yml`: Production stack with scaled concurrency, persistent volumes, and external Coolify network support.
  - `docker-compose.docs.yml`: Sphinx documentation server on port 9000.
- Added `.env.example` documenting all environment variables for services.
