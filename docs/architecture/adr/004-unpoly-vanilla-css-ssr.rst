ADR 004: SSR with Modern Vanilla CSS, Unpoly, and Web Components
==================================================================

Status
------
Accepted

Context
-------
Single Page Applications (SPAs) and heavy CSS utility compilers introduce complex toolchains (Node.js, npm/vite builds) and dual-state management. For Home-ERP, the goal is minimal dependencies, zero build-step overhead for static assets, high resilience, and fast development velocity.

Decision
--------
Adopt Django Server-Side Rendering (SSR) with standard Django template rendering, augmented with:
* **Modern Vanilla CSS**: Pure CSS leveraging native features:
  * Cascade layers (``@layer reset, tokens, base, layout, components, utilities``).
  * Design tokens using CSS Custom Properties (``--color-*``, ``--radius-*``, ``--font-*``).
  * Modern layouts via CSS Grid, Subgrid, and Flexbox.
  * Responsive modular components via Container Queries (``@container``).
* **Unpoly**: Unobtrusive server-driven interaction library:
  * Fragment updates (``up-target``), seamless link following (``up-follow``), and modal layers (``up-layer="new"``).
  * Out-of-the-box support for browser history, cache, loading states, and form validations (``up-validate``).
* **Vanilla JS & Web Components**: For self-contained interactive client widgets (e.g. quantity steppers, local charts, custom pickers) without external framework runtimes.

Consequences
------------
* **Positive**: Zero Node.js / npm build step required; standard Django template syntax (``{% include %}``, ``{% block %}``); native browser-grade styling capabilities; unified HTML-first mental model.
* **Negative**: Requires understanding of modern CSS cascade layers and Unpoly fragment lifecycle.
