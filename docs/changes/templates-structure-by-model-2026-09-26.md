# Change Summary: Template Directory Hierarchy by Model

**Date**: 2026-09-26  
**Type**: Architecture / Frontend  
**Scope**: `home_erp/apps/*/templates/`

## Key Additions

- **Modular Template Organization**:
  - Implemented the requested 3-tier structure inside each application:
    - `<app_label>/views/<model>/`
    - `<app_label>/partials/<model>/`
    - `<app_label>/components/`
- **Collision-Proof Django Namespacing**:
  - Maintained `<app_label>` root within `templates/` to comply with Django `APP_DIRS` lookup without template name collision across apps.
- **Coverage**:
  - Scaffolded 80 model-specific directories across all 16 applications in `tenant_apps`, `common_apps`, and `admin_apps`.
