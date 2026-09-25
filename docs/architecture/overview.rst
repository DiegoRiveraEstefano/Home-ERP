System Architecture & Principles
=================================

Context & Purpose
-----------------
Home-ERP adapts modular architecture concepts originally drafted for enterprise software into an agile, robust domestic platform. Instead of complex distributed microservices, Home-ERP implements a **Modular Monolith** built on Python 3.12+ and Django 5.x.

Key Principles
--------------

1. **Modular Monolith**:
   Code is partitioned into distinct bounded contexts (Django apps) with explicit module boundaries. Communication between apps is achieved via public service interfaces or internal signals rather than direct model mutations.

2. **12-Factor App Compliance**:
   All configuration is injected via environment variables (using ``django-environ``). Backing services like PostgreSQL and Redis are attached resources, ensuring portable execution across developer laptops, Docker containers, and home servers.

3. **Stateless Processes**:
   The web server process stores no persistent data on local disk. Uploaded media (receipt scans, appliance warranties) is delegated to Django's storage layer (local volume or S3-compatible object storage).

4. **Robust Domestic Transactions**:
   Domestic workflows involving multiple models (e.g., recording an expense while updating an account balance and checking budget caps) must be wrapped in atomic transactions (``transaction.atomic()``) to prevent partial writes.

Component Layout
----------------

* **Web Layer**: Thin Django class-based views (CBVs) handling HTTP protocol tasks, authentication, and standard template rendering enhanced with Unpoly fragment updates.
* **Service Layer**: Business workflows, domain validations, and mutation pipelines (stateless ``@classmethod`` functions).
* **Selector Layer**: Optimized read queries with explicit ``select_related`` and ``prefetch_related`` calls to prevent N+1 queries.
* **Data Layer**: PostgreSQL database with UUIDv7 primary keys, tenant scoping, and audit timestamp tracking.
* **Frontend Layer**: Modern Vanilla CSS structured via ``@layer`` with native design tokens, Unpoly for server-driven interactions, and Vanilla JS / Web Components for specialized client widgets.
