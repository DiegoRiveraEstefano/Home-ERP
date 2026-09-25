ADR 001: Modular Monolith on Django
====================================

Status
------
Accepted

Context
-------
Initial conceptual notes (`notas/v2`) targeted an enterprise multi-tier micro-service or multi-schema architecture in Java and Spring Boot. For Home-ERP, the focus shifts to domestic management (finances, inventory, chores, maintenance) requiring low operational overhead, single-container deployment, and rapid evolution.

Decision
--------
Adopt Python 3.12+ and Django 5.x as a Modular Monolith.
Individual domains (households, finances, inventory, assets, chores) are packaged as separate Django apps within the project repository. Cross-module communication is mediated through service classes and signals.

Consequences
------------
* **Positive**: Drastically reduced complexity; unified database transactions; single deployment artifact; native Django admin and ORM capabilities.
* **Negative**: Requires discipline to prevent cross-app circular imports and model coupling.
