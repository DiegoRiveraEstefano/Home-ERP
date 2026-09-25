ADR 002: Cookiecutter-Django Project Structure
==============================================

Status
------
Accepted

Context
-------
A standardized layout is required to support multiple environments (local development, production, CI testing), static asset organization, and separation of third-party vs. local apps.

Decision
--------
Structure the Home-ERP repository using the established `cookiecutter-django` baseline:
* Root configuration under `config/settings/` (`base.py`, `local.py`, `production.py`, `test.py`).
* All application code consolidated under `home_erp/`.
* Backing services configured via Docker Compose (`docker-compose.local.yml`, `docker-compose.production.yml`).
* Static assets organized under standard `home_erp/static/` with pure CSS and JS (zero build tooling required).

Consequences
------------
* **Positive**: Battle-tested 12-factor configuration; seamless Docker setup; out-of-the-box user model and authentication fixtures; no node/npm build dependencies for CSS or JS.
* **Negative**: Baseline template contains features that require trimming (e.g., removing unneeded SaaS plugins).
