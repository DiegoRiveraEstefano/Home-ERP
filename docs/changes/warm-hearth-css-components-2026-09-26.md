# Change Summary: Warm Hearth Design System CSS and Common UI Components

**Date**: 2026-09-26  
**Type**: Frontend / UI  
**Scope**: `home_erp/static/css/`, `home_erp/templates/components/`, `home_erp/templates/base.html`, `home_erp/static/js/components/`

## Key Additions

- **Warm Hearth Modern Vanilla CSS**:
  - Implemented zero-build native CSS layer hierarchy: `@layer reset, tokens, base, layout, components, utilities;`.
  - Added `home_erp/static/css/tokens.css` with domestic color palette (oat canvas, terracotta, sage green, warm wheat, brick rose) and comprehensive dark mode support (`[data-theme="dark"]`).
  - Added `home_erp/static/css/reset.css` for universal responsive baseline reset.
  - Added `home_erp/static/css/base.css` styling native HTML tags (`h1`-`h6`, `input`, `select`, `table`, `dialog`, `details`) out of the box with 44px minimum touch targets.
  - Added `home_erp/static/css/layout.css` providing `.app-shell`, sticky `.app-header`, responsive `.app-sidebar`, and `.grid-dashboard`.
  - Added `home_erp/static/css/components.css` with `.btn`, `.card`, `.badge`, `.metric-card`, `.data-table-container`, `.stepper`, `.alert`, `.empty-state`, `.avatar`, `.breadcrumbs`, `.tabs`, and `.dropdown`.
  - Added `home_erp/static/css/utilities.css` for accessibility (`.sr-only`), text truncations, and flex helpers.
  - Added `home_erp/static/css/main.css` entrypoint importing all layers.
- **Common Reusable UI Components**:
  - Scaffolded and implemented 19 standard Django component templates in `home_erp/templates/components/`:
    - `action/`: `button.html`, `dropdown.html`.
    - `data/`: `badge.html`, `card.html`, `metric_card.html`, `data_table.html`, `empty_state.html`.
    - `forms/`: `input.html`, `select.html`, `checkbox.html`, `stepper.html`.
    - `misc/`: `alert.html`, `avatar.html`, `modal.html`, `theme_toggle.html`.
    - `nav/`: `navbar.html`, `sidebar.html`, `breadcrumbs.html`, `tabs.html`, `pagination.html`.
- **Root Template and Interactivity**:
  - Implemented `home_erp/templates/base.html` with anti-flash theme detection, Google Fonts, Unpoly CSRF token handling, and Django message alerts.
  - Implemented layout variants: `base_dashboard.html`, `base_auth.html`, `base_landing.html`.
  - Added native Web Component `home_erp/static/js/components/stepper.js` (`<quantity-stepper>`).
