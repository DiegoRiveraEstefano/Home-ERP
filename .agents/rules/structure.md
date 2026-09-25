---
trigger: always_on
---

## Home-ERP: Directory Architecture (12-Factor App)

Modular monolithic Django project based on the Cookiecutter-Django layout.

### Repository Root Structure

```text
home-erp/
  .env, .env.example            # Factor III: Env vars & template
  .gitignore, .editorconfig     # Consistency & ignores
  pyproject.toml, uv.lock       # Factor II: Explicit dependencies
  README.md, CHANGELOG.md, AGENTS.md, manage.py
  docker-compose.local.yml, docker-compose.production.yml
  docs/                         # Sphinx documentation (architecture/, specs/, development/, adr/)
  locale/                       # i18n catalogs
  tests/                        # Root-level suite: unit/, integration/
  config/                       # Django project config (DJANGO_SETTINGS_MODULE=config.settings.<env>)
    settings/                   # base.py, local.py, production.py, test.py
    urls.py, api_router.py      # HTTP & API routing
    celery_app.py               # Celery app configuration
    asgi.py, wsgi.py            # ASGI/WSGI entry points
  home_erp/                     # Python package root - all application code lives here
    apps/                       # Domestic Domains (Bounded Contexts)
      households/               # Tenancy, members, invites, roles
      finances/                 # Accounts, transactions, budgets, bills
      inventory/                # Pantry, batches, locations, shopping lists
      assets/                   # Appliances, durable goods, maintenance logs
      chores/                   # Domestic tasks, rotations, assignments
      users/                    # User authentication and profile
      core/                     # Shared models, exceptions, mixins, tenancy managers
    templates/                  # Global SSR templates (base.html, layout/)
    static/                     # Static assets (zero build step)
      css/                      # Modern Vanilla CSS (@layer, tokens, layout, components)
      js/                       # Unpoly scripts, Vanilla JS, Web Components
      images/                   # Static icons, logos
    conftest.py
```

### Domain Apps (`home_erp/apps/`)

Registered as `home_erp.apps.<name>` in `LOCAL_APPS` (in `config/settings/base.py`):
`households`, `finances`, `inventory`, `assets`, `chores`, `users`, `core`.

### Core Shared Infrastructure (`home_erp/apps/core/`)

Shared components across domestic domains:
- `models.py`: `HouseholdScopedModel`, base UUIDv7 model, timestamp mixins.
- `managers.py`: `HouseholdScopedManager` for automatic tenancy filtering.
- `mixins.py`: `HouseholdContextMixin`, `PermissionRequiredMixin`.
- `exceptions.py`: `BusinessLogicError`, `InsufficientStockError`, `BudgetExceededError`.
- `services.py`, `utils.py`.

### Internal App Organization (Service Layer Pattern)

Prevents coupling and N+1 query bottlenecks.

```text
home_erp/apps/finances/
  __init__.py, admin.py, apps.py, urls.py   # App config & routing
  models.py                                 # DB models (thin schema + __str__)
  services/                                 # Write operations & atomic transactions
    expense_service.py, budget_service.py
  selectors.py                              # Complex read queries & prefetching (fixes N+1)
  views/                                    # Thin HTTP controllers
    accounts.py, expenses.py, budgets.py
  forms.py, filters.py, choices.py          # Input validation, forms, enums
  exceptions.py, signals.py                 # Domain errors & events
  migrations/                               # DB migrations
  templates/finances/                       # App-scoped templates ({% include %}, {% block %})
  tests/                                    # test_services.py, test_selectors.py
```

### Layer Responsibilities

| Layer | Responsibility | Home-ERP Benefit |
|---|---|---|
| `models.py` | Schema definition, relationships, simple string representations. | Clean ORM. Row-level household isolation via `HouseholdScopedModel`. |
| `services/` | Business rules, state changes, validations. | Reuse across web views, Celery workers, and CLI commands via `transaction.atomic()`. |
| `selectors.py` | Data reading: filters, aggregations, `prefetch_related`. | Isolates queries, prevents N+1 regressions. |
| `views/` | Unpack request parameters, call services/selectors, render responses. | Keeps controllers thin, testable, and focused. |
| `tasks.py` | Background jobs (e.g., daily chore rotation, bill reminders). | Complies with Factor VI (stateless async execution). |

### Background Tasks (Celery)

Queues defined in `config/settings/base.py`:
- `default`: Notifications, emails, routine assignments.
- `heavy`: Backup generation, receipt OCR analysis, data exports.
Schedules live in `CELERY_BEAT_SCHEDULE` (e.g., `generate-daily-chores-at-midnight`).

### 12-Factor Configuration

```python
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = BASE_DIR / "home_erp"
env = environ.Env()
env.read_env(str(BASE_DIR / ".env"))

DEBUG = env.bool("DJANGO_DEBUG", False)
DATABASES = {"default": env.db("DATABASE_URL", default="postgres:///home_erp")}
```
