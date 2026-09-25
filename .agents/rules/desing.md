---
trigger: always_on
description: Modern Vanilla CSS design system, tokens, cascade layers, and layout standards for Home-ERP.
---

# Home-ERP Design System (Modern Vanilla CSS)

## Overview

Home-ERP employs an accessible, high-density domestic dashboard design system implemented entirely in **Modern Vanilla CSS**. It uses native browser capabilities with zero build steps or preprocessors:
- Cascade Layers (`@layer`) for explicit specificity control.
- CSS Custom Properties (Design Tokens) for theme management and automatic dark mode.
- CSS Grid, Subgrid, and Flexbox for domestic data structures.
- Container Queries (`@container`) for responsive cards and dashboard widgets.

## Cascade Layer Architecture

All stylesheets declare and adhere to the following layer order:

```css
@layer reset, tokens, base, layout, components, utilities;
```

1. **`reset`**: Modern CSS baseline reset (box-sizing border-box, margin resets, responsive media defaults).
2. **`tokens`**: CSS custom properties for colors, typography, spacing, elevations, and radii.
3. **`base`**: HTML element defaults (body, headings, forms, tables, links).
4. **`layout`**: Grid systems, sidebars, headers, shell layout (`.app-shell`, `.grid-dashboard`).
5. **`components`**: Encapsulated UI components (`.card`, `.btn`, `.data-table`, `.dialog`).
6. **`utilities`**: Targeted overrides and helper classes (`.sr-only`, `.truncate`).

## Design Tokens (`@layer tokens`)

Tokens are declared on `:root` and adapted for dark mode via `[data-theme="dark"]` or `@media (prefers-color-scheme: dark)`.

### Core Color Palette

```css
@layer tokens {
  :root {
    /* Brand & Primary Actions */
    --color-primary: #2563eb;
    --color-primary-hover: #1d4ed8;

    /* Semantic Status */
    --color-success: #10b981;
    --color-danger: #dc2626;
    --color-warning: #f59e0b;

    /* Surfaces & Backgrounds */
    --color-bg-canvas: #f8fafc;
    --color-bg-surface: #ffffff;
    --color-bg-surface-input: #f1f5f9;
    --color-border-subtle: #e2e8f0;

    /* Text */
    --color-text-primary: #0f172a;
    --color-text-secondary: #475569;
    --color-text-muted: #64748b;
    --color-text-subtle: #94a3b8;

    /* Radii */
    --radius-atom: 12px;
    --radius-container: 24px;

    /* Typography */
    --font-sans: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  }

  [data-theme="dark"] {
    --color-primary: #3b82f6;
    --color-primary-hover: #60a5fa;
    --color-success: #34d399;
    --color-danger: #f87171;
    --color-warning: #fbbf24;

    --color-bg-canvas: #020617;
    --color-bg-surface: #0f172a;
    --color-bg-surface-input: #1e293b;
    --color-border-subtle: #1e293b;

    --color-text-primary: #f8fafc;
    --color-text-secondary: #cbd5e1;
    --color-text-muted: #94a3b8;
    --color-text-subtle: #64748b;
  }
}
```

## Layout Systems (`@layer layout`)

- **Dashboard Grids**: Use standard CSS Grid with `repeat(auto-fit, minmax(280px, 1fr))` for responsive metric cards.
- **Subgrid**: Align multi-column forms and nested list items using `grid-template-columns: subgrid`.
- **Container Queries**:
  ```css
  .card-container {
    container-type: inline-size;
  }

  @container (min-width: 480px) {
    .pantry-card {
      display: grid;
      grid-template-columns: 80px 1fr auto;
    }
  }
  ```

## Component Architecture (`@layer components`)

### Buttons (`.btn`)
```css
@layer components {
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.625rem 1.25rem;
    border-radius: var(--radius-atom);
    font-weight: 600;
    font-size: 0.875rem;
    border: 1px solid transparent;
    cursor: pointer;
    transition: background-color 150ms ease, border-color 150ms ease;
  }

  .btn-primary {
    background-color: var(--color-primary);
    color: #ffffff;
  }

  .btn-primary:hover {
    background-color: var(--color-primary-hover);
  }
}
```

### Data Tables (`.data-table`)
- Use native HTML `<table>` wrapped in `.data-table-container`.
- Fixed header with uppercase micro-typography (`text-transform: uppercase`, `letter-spacing: 0.05em`).
- Zebra row stripes opt-in via `.data-table--zebra`.

## Rules

- Always place CSS inside explicit `@layer` declarations.
- Never hardcode raw hex or RGB colors outside the `@layer tokens` block.
- Use CSS Custom Properties for all styling variables.
- Maintain a minimum touch target of 44x44px for domestic mobile inputs.
