# Home-ERP

Home-ERP is a self-hosted modular Enterprise Resource Planning system tailored for domestic environments. It provides households with structured control over personal finances, domestic inventory, asset maintenance schedules, and domestic task delegation.

Built with Python and Django, Home-ERP adapts clean architecture principles and a modular monolith structure initiated from the Cookiecutter-Django baseline.

## Core Capabilities

- **Household Management**: Multi-member household tenancy, role-based access control (Owner, Member, Guest), and activity logs.
- **Domestic Finances**: Double-entry ledger core, personal bank accounts, budget caps, expense classification, and recurring bill tracking.
- **Pantry & Inventory**: Household item tracking, unit conversions, batch and expiration date monitoring, storage location management, and low-stock replenishment alerts.
- **Assets & Maintenance**: Appliance and tool inventory, warranty document tracking, recurring maintenance schedules, and service histories.
- **Chores & Schedules**: Domestic task distribution, recurrence engines, assignment rotation, and completion auditing.

## Technology Stack

- **Backend**: Python 3.12+, Django 5.x
- **Persistence**: PostgreSQL (UUIDv7 primary keys, row-level household scoping)
- **Caching & Async**: Redis, Celery
- **Frontend**: Django Server-Side Rendering (SSR) with standard Django templates, Modern Vanilla CSS (`@layer`, custom properties, CSS Grid, container queries), Unpoly for server-driven interactions, and Vanilla JS / Web Components for specialized widgets
- **Logging**: Standard Python `logging` configured via Django settings
- **Tooling**: `uv` for fast dependency management, Docker Compose for local backing services

## Project Architecture

Home-ERP operates as a modular monolith adhering to 12-Factor principles:
- **Cookiecutter-Django Layout**: Separation of configuration, apps, static assets, and deployment environments.
- **Service Layer Pattern**: Thin models, stateless `@classmethod` services with transactional boundaries, and isolated `selectors.py` for read queries.
- **Strict Household Scoping**: Every business entity is bound to a `household_id`. Cross-household data access is blocked at the ORM and service layers.

## Repository Map

```text
.
├── .agents/rules/          # AI agent operational guidelines and engineering constraints
├── docs/                   # Full technical specification and architecture documentation (Sphinx / RST)
├── AGENTS.md               # Directives for autonomous and assisted development agents
├── CHANGELOG.md            # Release log adhering to Keep a Changelog standards
├── CONTEXT.md              # Domain context and bounded contexts
├── CONTRIBUTING.md         # Contribution and code review guidelines
├── DOCS.md                 # Documentation structure and Sphinx build instructions
├── GUIDELINES.md           # Engineering guidelines and architectural mandates
├── README.md               # Project overview (this document)
├── SECURITY.md             # Security disclosures and privacy boundaries
└── STYLE_GUIDE.md          # Code standards for Python, Django, Vanilla CSS, and Unpoly
```

## Quickstart

### Prerequisites
- Python 3.12+
- `uv` packaging manager
- Docker and Docker Compose (for PostgreSQL and Redis)

### Initial Setup
```bash
# Clone the repository
git clone https://github.com/DiegoRiveraEstefano/Home-ERP.git
cd Home-ERP

# Setup virtual environment and dependencies with uv
uv sync

# Launch backing services
docker compose -f docker-compose.local.yml up -d

# Run database migrations
uv run python manage.py migrate

# Start local development server
uv run python manage.py runserver
```

## License

This project is licensed under the terms defined in [LICENSE](file:///home/diego/Proyectos/Home-ERP/LICENSE).