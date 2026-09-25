---
trigger: always_on
description: Modern Vanilla CSS design system (Warm Hearth palette, cascade layers, base HTML styles, component classes).
---

# Home-ERP Design System: Warm Hearth (Modern Vanilla CSS)

## 1. Overview & Aesthetic Identity

Home-ERP departs from sterile corporate SaaS interfaces in favor of **Warm Hearth**: a domestic, tactile, and calm visual language. It takes inspiration from natural ceramic earthenware, warm linen notebooks, and organized pantry pantries.

The system is built entirely on native **Modern Vanilla CSS** with zero build steps or preprocessors:
- Cascade Layers (`@layer`) enforce strict specificity control.
- CSS Custom Properties (Design Tokens) manage colors, typography, elevations, and dark mode.
- Base HTML elements (`<form>`, `<input>`, `<table>`, `<dialog>`) provide complete styling out of the box with zero required utility classes.
- Explicit component classes (`.card`, `.btn`, `.badge`, `.data-table`, `.stepper`) encapsulate compound domestic UI widgets.

---

## 2. Cascade Layer Architecture

All stylesheets adhere to the following layer sequence:

```css
@layer reset, tokens, base, layout, components, utilities;
```

1. **`reset`**: Universal box-sizing, margin resets, responsive media defaults.
2. **`tokens`**: Theme custom properties (colors, typography, radii, spacing, elevation).
3. **`base`**: Out-of-the-box styling for native HTML elements (headings, inputs, tables, dialogs).
4. **`layout`**: App shell, domestic dashboard grids, container query contexts.
5. **`components`**: Reusable component classes (`.card`, `.btn`, `.badge`, `.data-table`, `.stepper`).
6. **`utilities`**: Targeted utility helper classes (`.sr-only`, `.truncate`, `.text-center`).

---

## 3. Design Tokens (`@layer tokens`)

### Color Palette & Theme Tokens

```css
@layer tokens {
  :root {
    /* Surfaces & Canvas */
    --color-bg-canvas: #FAF6F0;       /* Warm oat canvas */
    --color-bg-surface: #FFFFFF;      /* Ivory white surface */
    --color-bg-surface-warm: #F4EFE6; /* Warm sand for subtle depth */
    --color-bg-input: #F7F3EC;        /* Soft input surface */
    --color-border-subtle: #E8E0D5;   /* Warm hairline boundary */
    --color-border-strong: #D4C9BC;   /* Structured divider */
    --color-border-focus: #C87D55;    /* Terracotta focus ring */

    /* Brand & Domestic Status */
    --color-primary: #C87D55;         /* Warm terracotta */
    --color-primary-hover: #B56B44;
    --color-primary-light: #F7ECE4;   /* Soft terracotta tint */
    --color-secondary: #87A987;       /* Sage green */
    --color-secondary-light: #EDF3ED;
    --color-warning: #E9C46A;         /* Warm wheat */
    --color-warning-light: #FCF7EB;
    --color-danger: #D96B6B;          /* Soft brick rose */
    --color-danger-light: #FBEFEF;
    --color-info: #789BB5;            /* Slate denim */
    --color-info-light: #EDF3F7;

    /* Text & Typography */
    --color-text-primary: #2E2A27;    /* Soft charcoal */
    --color-text-secondary: #5C554F;  /* Warm stone */
    --color-text-muted: #8A8178;      /* Dried clay */
    --color-text-inverse: #FFFFFF;

    /* Typography */
    --font-serif: "Newsreader", "Fraunces", Georgia, serif;
    --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

    /* Radii */
    --radius-atom: 10px;              /* Buttons, inputs, chips */
    --radius-card: 18px;              /* Cards, panels, dialogs */
    --radius-pill: 9999px;            /* Badges, pill toggles */

    /* Shadows & Elevation */
    --shadow-sm: 0 1px 3px rgba(46, 42, 39, 0.05);
    --shadow-card: 0 4px 12px rgba(46, 42, 39, 0.04), 0 1px 3px rgba(46, 42, 39, 0.03);
    --shadow-dialog: 0 12px 32px rgba(46, 42, 39, 0.12);

    /* Spacing Units */
    --space-xs: 0.25rem;
    --space-sm: 0.5rem;
    --space-md: 1rem;
    --space-lg: 1.5rem;
    --space-xl: 2rem;
  }

  [data-theme="dark"] {
    --color-bg-canvas: #1A1816;
    --color-bg-surface: #24211E;
    --color-bg-surface-warm: #2C2825;
    --color-bg-input: #2D2926;
    --color-border-subtle: #38332E;
    --color-border-strong: #4A443E;
    --color-border-focus: #D98C64;

    --color-primary: #D98C64;
    --color-primary-hover: #E69D76;
    --color-primary-light: #382820;
    --color-secondary: #97B897;
    --color-secondary-light: #243024;
    --color-warning: #F0CF7D;
    --color-warning-light: #38311F;
    --color-danger: #E27B7B;
    --color-danger-light: #382020;
    --color-info: #8AAEC7;
    --color-info-light: #202A33;

    --color-text-primary: #F5EFE6;
    --color-text-secondary: #C8BFB5;
    --color-text-muted: #9E948A;
    --color-text-inverse: #1A1816;

    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
    --shadow-card: 0 4px 12px rgba(0, 0, 0, 0.25);
    --shadow-dialog: 0 12px 32px rgba(0, 0, 0, 0.5);
  }
}
```

---

## 4. Modern CSS Reset (`@layer reset`)

```css
@layer reset {
  *, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  html {
    -webkit-text-size-adjust: 100%;
    tab-size: 4;
    font-feature-settings: normal;
    scroll-behavior: smooth;
  }

  body {
    min-height: 100vh;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  img, picture, video, canvas, svg {
    display: block;
    max-width: 100%;
    height: auto;
  }

  input, button, textarea, select {
    font: inherit;
    color: inherit;
  }

  table {
    border-collapse: collapse;
    border-spacing: 0;
  }
}
```

---

## 5. Base HTML Element Defaults (`@layer base`)

HTML elements look clean and styled out of the box without utility classes:

### Typography
- `body`: Uses `--font-sans`, `--color-bg-canvas`, and `--color-text-primary`.
- `h1, h2, h3, h4`: Use `--font-serif` with soft line heights and natural margins.
- `p`: Margined with `0 0 1rem 0`, constrained to a comfortable reading line length (`max-width: 70ch`).
- `a`: Colored with `--color-primary`, subtle text-underline-offset (`0.2em`).

### Form Elements
- `form`: Flex or grid with natural gap rhythm (`var(--space-md)`).
- `input[type="text"]`, `input[type="email"]`, `input[type="number"]`, `input[type="date"]`, `select`, `textarea`:
  - Background: `var(--color-bg-input)`.
  - Border: `1px solid var(--color-border-subtle)`.
  - Border radius: `var(--radius-atom)`.
  - Padding: `0.625rem 0.875rem`.
  - Focus state: `outline: 2px solid var(--color-border-focus); border-color: transparent;`.
  - Minimum touch target: `44px` height.
- `label`: Block display, `font-weight: 600`, font size `0.875rem`, color `var(--color-text-secondary)`, bottom margin `0.375rem`.

### Tables
- `table`: Width `100%`, border-collapse `collapse`.
- `th`: Background `var(--color-bg-surface-warm)`, color `var(--color-text-secondary)`, uppercase micro-typography (`font-size: 0.75rem`, `letter-spacing: 0.05em`), padding `0.75rem 1rem`.
- `td`: Padding `0.875rem 1rem`, border-bottom `1px solid var(--color-border-subtle)`.

### Dialogs
- `dialog`:
  - Background: `var(--color-bg-surface)`.
  - Border: `1px solid var(--color-border-subtle)`.
  - Border radius: `var(--radius-card)`.
  - Box shadow: `var(--shadow-dialog)`.
  - Padding: `var(--space-xl)`.
  - `&::backdrop`: `background: rgba(46, 42, 39, 0.4); backdrop-filter: blur(4px);`.

---

## 6. Reusable Component Classes (`@layer components`)

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
    line-height: 1.25;
    border: 1px solid transparent;
    cursor: pointer;
    text-decoration: none;
    transition: background-color 150ms ease, border-color 150ms ease, transform 100ms ease;
  }

  .btn:active {
    transform: scale(0.98);
  }

  .btn-primary {
    background-color: var(--color-primary);
    color: var(--color-text-inverse);
  }
  .btn-primary:hover {
    background-color: var(--color-primary-hover);
  }

  .btn-secondary {
    background-color: var(--color-secondary-light);
    color: var(--color-secondary);
    border-color: var(--color-secondary);
  }

  .btn-outline {
    background-color: transparent;
    border-color: var(--color-border-strong);
    color: var(--color-text-primary);
  }
  .btn-outline:hover {
    background-color: var(--color-bg-surface-warm);
  }

  .btn-ghost {
    background-color: transparent;
    color: var(--color-text-secondary);
  }
  .btn-ghost:hover {
    background-color: var(--color-bg-surface-warm);
    color: var(--color-text-primary);
  }
}
```

### Cards (`.card`)
```css
@layer components {
  .card {
    background-color: var(--color-bg-surface);
    border: 1px solid var(--color-border-subtle);
    border-radius: var(--radius-card);
    padding: var(--space-lg);
    box-shadow: var(--shadow-card);
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--space-md);
    padding-bottom: var(--space-sm);
    border-bottom: 1px solid var(--color-border-subtle);
  }

  .card-title {
    font-family: var(--font-serif);
    font-size: 1.25rem;
    color: var(--color-text-primary);
  }
}
```

### Status Badges (`.badge`)
```css
@layer components {
  .badge {
    display: inline-flex;
    align-items: center;
    gap: 0.375rem;
    padding: 0.25rem 0.625rem;
    border-radius: var(--radius-pill);
    font-size: 0.75rem;
    font-weight: 600;
    line-height: 1;
  }

  .badge-success {
    background-color: var(--color-secondary-light);
    color: var(--color-secondary);
  }

  .badge-warning {
    background-color: var(--color-warning-light);
    color: #946E1E;
  }

  .badge-danger {
    background-color: var(--color-danger-light);
    color: var(--color-danger);
  }

  .badge-terracotta {
    background-color: var(--color-primary-light);
    color: var(--color-primary);
  }
}
```

### Domestic Metric Card (`.metric-card`)
```css
@layer components {
  .metric-card {
    background-color: var(--color-bg-surface);
    border: 1px solid var(--color-border-subtle);
    border-radius: var(--radius-card);
    padding: var(--space-md) var(--space-lg);
    display: flex;
    flex-direction: column;
    gap: var(--space-xs);
  }

  .metric-label {
    font-size: 0.8125rem;
    color: var(--color-text-muted);
    font-weight: 500;
  }

  .metric-value {
    font-family: var(--font-serif);
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--color-text-primary);
    line-height: 1.2;
  }
}
```

### Data Table Container (`.data-table-container`)
```css
@layer components {
  .data-table-container {
    background-color: var(--color-bg-surface);
    border: 1px solid var(--color-border-subtle);
    border-radius: var(--radius-card);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
  }

  .data-table--zebra tbody tr:nth-child(even) {
    background-color: var(--color-bg-canvas);
  }

  .data-table tbody tr:hover {
    background-color: var(--color-bg-surface-warm);
  }
}
```

### Tactile Quantity Stepper (`.stepper`)
```css
@layer components {
  .stepper {
    display: inline-flex;
    align-items: center;
    border: 1px solid var(--color-border-subtle);
    border-radius: var(--radius-atom);
    background-color: var(--color-bg-input);
    overflow: hidden;
  }

  .stepper-btn {
    padding: 0.5rem 0.75rem;
    background: transparent;
    border: none;
    cursor: pointer;
    color: var(--color-text-primary);
    font-weight: bold;
  }

  .stepper-btn:hover {
    background-color: var(--color-bg-surface-warm);
  }

  .stepper-value {
    padding: 0.25rem 0.5rem;
    font-weight: 600;
    min-width: 2.5rem;
    text-align: center;
  }
}
```

---

## 7. Layout Systems (`@layer layout`)

### App Shell
```css
@layer layout {
  .app-shell {
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    min-height: 100vh;
  }

  @media (min-width: 768px) {
    .app-shell {
      grid-template-columns: 240px minmax(0, 1fr);
    }
  }

  .app-sidebar {
    background-color: var(--color-bg-surface);
    border-right: 1px solid var(--color-border-subtle);
    padding: var(--space-lg);
  }

  .app-main {
    padding: var(--space-lg);
    background-color: var(--color-bg-canvas);
  }
}
```

### Dashboard Grid
```css
@layer layout {
  .grid-dashboard {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: var(--space-lg);
  }
}
```

---

## 8. Development Rules

1. Place every CSS rule inside its appropriate `@layer` (`reset`, `tokens`, `base`, `layout`, `components`, `utilities`).
2. Never hardcode raw hex, rgb, or hsl colors outside `@layer tokens`.
3. Leverage base element styling before introducing new component classes.
4. Maintain minimum touch targets of 44x44px for domestic mobile inputs and buttons.
