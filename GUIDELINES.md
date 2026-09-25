# Engineering Guidelines (GUIDELINES.md)

Home-ERP adheres to 12-Factor application principles adapted for domestic self-hosted and cloud deployments.

## 12-Factor Principles in Home-ERP

1. **Codebase**: One codebase tracked in revision control, many deploys (local, staging, home server).
2. **Dependencies**: Explicitly declared and isolated using `uv` and `pyproject.toml`. No system-wide package assumptions.
3. **Config**: Strict separation of config from code via environment variables (`django-environ`). Database credentials, Redis URLs, and secrets are read via environment.
4. **Backing Services**: Datastores (PostgreSQL), caches (Redis), and media storages (local or S3-compatible) are treated as attached resources.
5. **Build, Release, Run**: Clear separation between dependency installation, configuration injection, and execution.
6. **Processes**: The application executes as stateless processes. Ephemeral files in `/tmp` are forbidden for persistent data. Uploaded receipts and warranties must be stored via Django's default storage backend.
7. **Port Binding**: Self-contained web services exporting HTTP via Daphne/Uvicorn/Gunicorn.
8. **Concurrency**: Scale through process models (web workers, Celery workers for async background jobs).
9. **Disposability**: Fast startup and graceful shutdown. All multi-step mutations must be wrapped in `transaction.atomic()` to guarantee rollback on process termination.
10. **Dev/Prod Parity**: Keep development, staging, and production as similar as possible. PostgreSQL is used in both development and production.
11. **Logs**: Treat logs as event streams. Output structured logs to stdout using standard Python `logging` configured via Django settings.
12. **Admin Processes**: One-off administration tasks (migrations, data fixes, recurring chore generation) run as management commands (`python manage.py <command>`).

## Architectural Constraints

- **Single Responsibility**: Keep files below 400 lines. Split sprawling modules into dedicated service or selector packages.
- **Fail Early**: Employ guard clauses and early returns to keep happy paths left-aligned.
- **Zero Business Logic in Views**: Controllers only unpack input, authorize, call services/selectors, and render responses.
- **Frontend Simplicity**: Rely on Modern Vanilla CSS with `@layer`, standard Django template rendering, Unpoly for server-driven UI, and Vanilla JS / Web Components for stateful widgets.
