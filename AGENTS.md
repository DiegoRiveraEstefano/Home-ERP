# Agent Operational Directives (AGENTS.md)

This document defines execution rules and domain boundaries for automated agents interacting with the Home-ERP repository.

## Operational Principles

1. **Adherence to Domain Boundaries**: Home-ERP is a domestic ERP system. Do not introduce enterprise B2B concepts (such as POS cashiers, tax authority integrations like SII, commercial credit limits, or SaaS billing modules) unless explicitly requested.
2. **Deterministic Architecture**:
   - Web controllers (`views/`) remain thin. Unpack HTTP parameters, call services or selectors, and return templates or JSON responses.
   - Mutations and business workflows belong exclusively in `services/` (`@classmethod` methods wrapped in `transaction.atomic()`).
   - Read logic, data aggregation, and query optimizations belong exclusively in `selectors.py`.
3. **Mandatory Household Scoping**: Every business entity and service method requires an explicit `household_id`. Global queries without household filters are strictly prohibited.
4. **Minimal Diff Wins**: Follow lazy senior developer principles. Do not add speculative abstractions, unrequested dependencies, or boilerplate.

## Rule Files Reference

All agents must follow rules located in `.agents/rules/`:
- `architecture.md`: 12-Factor app requirements, atomic boundaries, and backing services.
- `structure.md`: Directory layout and modular monolith boundaries.
- `services.py` / `services.md`: Stateless service layer constraints and signatures.
- `code_style.md`: Guard clauses, early returns, cyclomatic complexity limits.
- `tdd.md`: Test-driven development with `pytest`, isolation checks, and N+1 prevention.
- `desing.md`: Modern Vanilla CSS design tokens, layers, and responsive domestic layout.
- `logs.md`: Structured logging via Python standard `logging` with domain identifiers.
- `templates.md`: Standard Django templates, Unpoly interactions, Vanilla JS, and Web Components.
- `views.md`: CBVs, mixins, and clean Unpoly fragment integration.

## Working with Documentation

When modifying core business models, service signatures, or architecture:
- Update corresponding `.rst` documents under `docs/`.
- Ensure all new `.rst` files are included in parent `toctree` directives.
- Record significant changes in a dated summary in `docs/changes/` before merging into `CHANGELOG.md`.
