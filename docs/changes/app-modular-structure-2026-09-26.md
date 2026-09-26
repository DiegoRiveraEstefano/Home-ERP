# Change Summary: App Modular Structure & Service Layer Scaffolding

**Date**: 2026-09-26  
**Type**: Architecture / Feature  
**Scope**: `home_erp/apps/` (`tenant_apps`, `common_apps`, `admin_apps`)

## Key Additions

- **Standard Internal Organization Across 16 Apps**:
  - Implemented standard layout in each domain module:
    - `admin.py`, `apps.py`, `urls.py`, `models.py`, `choices.py`, `forms.py`, `filters.py`, `exceptions.py`, `signals.py`, `selectors.py`
    - `services/` directory with `@classmethod` and `@transaction.atomic` standard methods.
    - `views/` directory with CBVs.
    - `migrations/` directory with `__init__.py`.
    - `templates/<app_label>/` directory with `.gitkeep`.
    - `tests/` directory with `test_services.py` and `test_selectors.py`.
- **Tenant Scoping Guarantee**:
  - All tenant services in `tenant_apps` enforce `household_id: str | UUID` as the first parameter.
- **Django App Label Collision Prevention**:
  - Isolated labels for homonymous apps: `tenant_analytics` vs `admin_analytics`, and `admin_*` prefixes.
- **Shared Base Exceptions**:
  - Defined `BusinessLogicError` in `home_erp/shared/exceptions/__init__.py`.
