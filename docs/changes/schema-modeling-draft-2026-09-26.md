# Change Summary: Database Schema Modeling Draft

**Date**: 2026-09-26  
**Type**: Feature / Architecture  
**Scope**: `docs/architecture/schema_draft.sql`

## Key Additions & Modeling Decisions

- **Household Multi-Tenancy & Isolation**:
  - Direct row-level tenancy enforcement across all 18 domestic entities via `household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE`.
- **Simple RBAC & Membership**:
  - `household_roles`: Standard roles (`OWNER`, `ADMIN`, `MEMBER`, `GUEST`).
  - `household_permissions`: Granular domestic capabilities across `households`, `inventory`, `finances`, `assets`, `chores`, and `audit`.
  - `household_role_permissions`: Association table preloaded with standard role mappings.
  - `household_members`: Unique user-to-household membership with roles, nickname, and timestamps.
  - `household_invitations`: Secure cryptographic token workflow with email, expiration, and status tracking (`PENDING`, `ACCEPTED`, `EXPIRED`, `REVOKED`).
  - `v_household_member_permissions`: Convenience SQL view resolving active members to granted capabilities.
- **Centralized Domestic Audit Log**:
  - `household_audit_logs`: Append-only activity ledger recording event category, action type, target entity, actor, summary, and contextual `JSONB` metadata (e.g. quantity consumed, invitation details, expense recorded).
  - High-performance indexes on `(household_id, created_at DESC)`, `(household_id, event_category)`, and GIN indexing on `metadata`.
- **Domain Modules**:
  - **Inventory & Despensa**: `storage_locations`, `item_categories`, `pantry_items`, `stock_batches` (with expiration tracking and depletion status), `shopping_list_items`.
  - **Finances**: `financial_accounts`, `transaction_categories` (hierarchical tree), `financial_transactions` (income/expense/transfer), `budgets` (monthly category limits), `recurring_bills`.
  - **Assets & Maintenance**: `assets`, `maintenance_schedules`, `maintenance_logs`.
  - **Chores & Tasks**: `chores`, `chore_assignments` with gamification points and rotation support.
