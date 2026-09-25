ADR 003: Row-Level Household Multi-Tenancy
==========================================

Status
------
Accepted

Context
-------
Enterprise tenancy designs from `notas/v2` specified dedicated database schemas and dynamic routing tiers. For domestic ERP, households are typically small entities (1 to 10 members). Separate schemas would create excessive migration overhead and operational friction.

Decision
--------
Implement shared-database, shared-schema tenancy with row-level filtering governed by `household_id`.
All domestic domain entities inherit from `HouseholdScopedModel`. Isolation is enforced by:
1. Custom model manager auto-filtering by the active household context.
2. Mandatory `household_id` parameters across all service and selector methods.
3. Database composite indexes on `(household_id, id)` and foreign key cascades.

Consequences
------------
* **Positive**: Simple migrations; trivial cross-household analytical reporting for superusers; lightweight footprint.
* **Negative**: Requires rigorous automated tests to ensure no queries leak across households.
