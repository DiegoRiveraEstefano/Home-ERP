Warm Hearth Design System
========================

Overview
--------
Home-ERP employs the **Warm Hearth** design system. Moving away from corporate SaaS aesthetics, Warm Hearth embraces an organic, domestic, and calming visual language inspired by natural terracotta earthenware, oat linen notebooks, and clean home spaces.

The design system is implemented in pure **Modern Vanilla CSS** with zero build steps or CSS compilers:
* **Cascade Layers (``@layer``)**: Explicit specificity control.
* **Design Tokens**: Standardized CSS Custom Properties on ``:root`` and ``[data-theme="dark"]``.
* **Classless Base Elements**: Native HTML elements (``<form>``, ``<input>``, ``<table>``, ``<dialog>``) look complete without utility classes.
* **Domestic UI Components**: Encapsulated component classes for compound widgets.

Cascade Layer Architecture
--------------------------

All stylesheets follow this explicit layer order:

.. code-block:: css

    @layer reset, tokens, base, layout, components, utilities;

* **``reset``**: Baseline resets (box-sizing border-box, margin resets, responsive media defaults).
* **``tokens``**: Custom properties defining colors, typography, radii, shadows, and spacing.
* **``base``**: Default styling for native HTML elements.
* **``layout``**: High-level shell layout, sidebars, dashboard grids, and container queries.
* **``components``**: Visual component classes (``.btn``, ``.card``, ``.badge``, ``.data-table``).
* **``utilities``**: Helper overrides (``.sr-only``, ``.truncate``).

Design Tokens
-------------

Color Palette
~~~~~~~~~~~~~

.. code-block:: css

    @layer tokens {
      :root {
        /* Canvas & Surfaces */
        --color-bg-canvas: #FAF6F0;       /* Warm oat canvas */
        --color-bg-surface: #FFFFFF;      /* Ivory surface */
        --color-bg-surface-warm: #F4EFE6; /* Warm sand */
        --color-bg-input: #F7F3EC;        /* Form input background */
        --color-border-subtle: #E8E0D5;   /* Hairline borders */
        --color-border-focus: #C87D55;    /* Terracotta focus ring */

        /* Brand & Status */
        --color-primary: #C87D55;         /* Terracotta */
        --color-primary-hover: #B56B44;
        --color-secondary: #87A987;       /* Sage green */
        --color-warning: #E9C46A;         /* Warm wheat */
        --color-danger: #D96B6B;          /* Soft brick rose */
        --color-info: #789BB5;            /* Slate denim */

        /* Typography */
        --color-text-primary: #2E2A27;    /* Soft charcoal */
        --color-text-secondary: #5C554F;  /* Warm stone */
        --color-text-muted: #8A8178;      /* Dried clay */

        /* Radii */
        --radius-atom: 10px;              /* Buttons, inputs */
        --radius-card: 18px;              /* Cards, dialogs */
        --radius-pill: 9999px;            /* Badges */

        /* Typography */
        --font-serif: "Newsreader", "Fraunces", Georgia, serif;
        --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      }

      [data-theme="dark"] {
        --color-bg-canvas: #1A1816;
        --color-bg-surface: #24211E;
        --color-bg-surface-warm: #2C2825;
        --color-bg-input: #2D2926;
        --color-border-subtle: #38332E;
        --color-border-focus: #D98C64;

        --color-primary: #D98C64;
        --color-secondary: #97B897;
        --color-warning: #F0CF7D;
        --color-danger: #E27B7B;
        --color-info: #8AAEC7;

        --color-text-primary: #F5EFE6;
        --color-text-secondary: #C8BFB5;
        --color-text-muted: #9E948A;
      }
    }

Base HTML Elements Contract
---------------------------

Native HTML tags are pre-styled in ``@layer base``:

1. **Headings (``h1`` to ``h4``)**: Rendered in ``var(--font-serif)`` with comfortable domestic line height and color ``var(--color-text-primary)``.
2. **Form Controls (``input``, ``select``, ``textarea``)**:
   * Automatic background: ``var(--color-bg-input)``.
   * Border: ``1px solid var(--color-border-subtle)``.
   * Corner radius: ``var(--radius-atom)``.
   * Minimum touch target: ``44px``.
   * Focus: ``outline: 2px solid var(--color-border-focus)``.
3. **Tables (``table``, ``thead``, ``tbody``)**:
   * Full width with collapsed borders.
   * Header background in ``var(--color-bg-surface-warm)`` with uppercase micro-typography.
4. **Dialogs (``dialog``)**:
   * Native ``<dialog>`` styled with ``var(--color-bg-surface)``, ``var(--radius-card)``, and warm frosted glass backdrop.

Component Class Catalog
-----------------------

Buttons (``.btn``)
~~~~~~~~~~~~~~~~~~
.. code-block:: html

    <button type="submit" class="btn btn-primary">Save Expense</button>
    <a href="/pantry/" class="btn btn-outline">Cancel</a>
    <button type="button" class="btn btn-ghost">Dismiss</button>

Cards (``.card``)
~~~~~~~~~~~~~~~~~
.. code-block:: html

    <div class="card">
      <div class="card-header">
        <h2 class="card-title">Pantry Quick Add</h2>
      </div>
      <div class="card-body">
        <form method="post">
          <!-- Form elements styled by default -->
        </form>
      </div>
    </div>

Status Badges (``.badge``)
~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: html

    <span class="badge badge-success">Completed</span>
    <span class="badge badge-warning">Expiring Soon</span>
    <span class="badge badge-danger">Overdue</span>
    <span class="badge badge-terracotta">Pending Review</span>

Metric Cards (``.metric-card``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: html

    <div class="metric-card">
      <span class="metric-label">Monthly Grocery Budget</span>
      <span class="metric-value">$420.00</span>
      <span class="badge badge-success">18% under limit</span>
    </div>

Data Tables (``.data-table-container``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: html

    <div class="data-table-container">
      <table class="data-table data-table--zebra">
        <thead>
          <tr>
            <th>Item</th>
            <th>Location</th>
            <th>Stock</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Organic Milk 1L</td>
            <td>Main Fridge</td>
            <td>2 units</td>
            <td><button class="btn btn-ghost">Use</button></td>
          </tr>
        </tbody>
      </table>
    </div>

Tactile Stepper (``.stepper``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: html

    <div class="stepper">
      <button type="button" class="stepper-btn" aria-label="Decrease">-</button>
      <span class="stepper-value">3</span>
      <button type="button" class="stepper-btn" aria-label="Increase">+</button>
    </div>
