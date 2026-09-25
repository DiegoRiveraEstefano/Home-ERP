---
trigger: always_on
---

# Home-ERP: Frontend (Unpoly, Web Components, Modern Vanilla CSS)

**Context:** Server-Side Rendering (SSR). Django renders HTML via built-in template inheritance; Modern Vanilla CSS structures visual styles; Unpoly drives progressive DOM updates; Vanilla JS and Web Components handle localized client interactivity.  
**Priority:** Semantic HTML > Modern Vanilla CSS (`@layer`) > Unpoly > Web Components > Vanilla JS.

## Rules

- **Standard Django Templates:** Use built-in Django template rendering (`{% extends %}`, `{% block %}`, `{% include %}`). Do not use external template component DSLs.
- **Semantic HTML:** Use native `<dialog>` for modals, `<details>/<summary>` for expandable panels, appropriate input types (`number`, `date`, `file`), and native form validation constraints (`required`, `min`, `max`).
- **Modern Vanilla CSS:** Place all rules inside cascade layers (`@layer reset, tokens, base, layout, components, utilities`). Use design tokens (`var(--color-primary)`).
- **Unpoly (Server-Driven Navigation & Fragments):**
  - Use `[up-follow]` on standard links for fast, animated fragment page navigation.
  - Use `[up-target]` to target specific DOM fragments to update without full reloads:
    ```html
    <a href="/inventory/items/?category=dairy" up-follow up-target="#pantry-list">Dairy Only</a>
    ```
  - Use `[up-layer="new modal"]` or `[up-modal]` for accessible server-rendered dialogs.
  - Use `[up-validate]` on form fields to trigger server validation before form submission.
- **Vanilla JS & Web Components:**
  - Build standalone, stateful client widgets (e.g. quantity steppers, barcode scanners, interactive charts) as native Web Components:
    ```javascript
    class StockStepper extends HTMLElement {
      connectedCallback() {
        // native DOM listeners
      }
    }
    customElements.define('stock-stepper', StockStepper);
    ```
  - Do not introduce external frontend frameworks (Vue, React, Alpine) for simple domestic controls.

## Anti-patterns vs. Best Practices

| Anti-pattern | Correct | Why |
|---|---|---|
| Heavy JavaScript modal with click listeners | Unpoly modal `[up-layer="new modal"]` or native `<dialog>` | Standard, accessible, server-driven |
| Manually fetching JSON and creating DOM elements in JS | Unpoly fragment swap `<a href="..." up-follow up-target="#table">` | Keeps rendering server-side |
| Inline style overrides `style="background: #2563eb"` | Semantic CSS class with design token `var(--color-primary)` | Theme and dark mode compliance |
| Custom component tag libraries | Standard Django `{% include "finances/partials/summary.html" %}` | Native Django capabilities, zero dependencies |