-- ==============================================================================
-- Home-ERP: Relational Schema Draft (PostgreSQL 16+)
-- Architecture: Domestic Modular ERP with Row-Level Household Tenancy
-- File: docs/architecture/schema_draft.sql
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. EXTENSIONS & GENERAL CONFIGURATION
-- ------------------------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Function to automatically update timestamp on record modification
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- ------------------------------------------------------------------------------
-- 2. USERS (Core Authentication & Identity)
-- ------------------------------------------------------------------------------
-- Represents individual human accounts in the system (maps to Django User model).
CREATE TABLE users_user (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(150) NOT NULL UNIQUE,
    email VARCHAR(254) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    name VARCHAR(255) NOT NULL DEFAULT '',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    date_joined TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_login TIMESTAMPTZ
);

COMMENT ON TABLE users_user IS 'Global application users capable of participating in one or more households.';


-- ------------------------------------------------------------------------------
-- 3. HOUSEHOLDS & SIMPLE RBAC (Tenancy Boundary)
-- ------------------------------------------------------------------------------
-- Root boundary for domestic tenancy. All domestic entities belong to a household.
CREATE TABLE households (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(120) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    timezone VARCHAR(50) NOT NULL DEFAULT 'UTC',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TRIGGER trg_households_updated_at
BEFORE UPDATE ON households
FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp();

COMMENT ON TABLE households IS 'Domestic tenancy boundary. Groups members and domestic data.';

-- RBAC: Predefined system roles for household members
CREATE TABLE household_roles (
    code VARCHAR(32) PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    hierarchy_level INT NOT NULL DEFAULT 100 -- Lower number = higher authority
);

COMMENT ON TABLE household_roles IS 'Standardized domestic role definitions (OWNER, ADMIN, MEMBER, GUEST).';

-- RBAC: Granular domestic permission definitions
CREATE TABLE household_permissions (
    code VARCHAR(64) PRIMARY KEY,
    module VARCHAR(32) NOT NULL, -- e.g. households, inventory, finances, assets, chores, audit
    name VARCHAR(128) NOT NULL,
    description TEXT NOT NULL DEFAULT ''
);

COMMENT ON TABLE household_permissions IS 'Granular action capabilities within a household.';

-- RBAC: Role to permission mapping
CREATE TABLE household_role_permissions (
    role_code VARCHAR(32) NOT NULL REFERENCES household_roles(code) ON DELETE CASCADE,
    permission_code VARCHAR(64) NOT NULL REFERENCES household_permissions(code) ON DELETE CASCADE,
    PRIMARY KEY (role_code, permission_code)
);

COMMENT ON TABLE household_role_permissions IS 'Mapping defining default capabilities granted to each role.';

-- Household Members: Relationship linking a User to a Household with an assigned Role
CREATE TABLE household_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users_user(id) ON DELETE CASCADE,
    role_code VARCHAR(32) NOT NULL REFERENCES household_roles(code) ON DELETE RESTRICT,
    nickname VARCHAR(64),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    joined_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_household_member UNIQUE (household_id, user_id)
);

CREATE INDEX idx_household_members_user ON household_members(user_id);
CREATE INDEX idx_household_members_household ON household_members(household_id);

CREATE TRIGGER trg_household_members_updated_at
BEFORE UPDATE ON household_members
FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp();

COMMENT ON TABLE household_members IS 'Active and historical member associations within a household.';

-- Household Invitations: Secure token-based onboarding for new members
CREATE TABLE household_invitations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    email VARCHAR(254) NOT NULL,
    role_code VARCHAR(32) NOT NULL REFERENCES household_roles(code) ON DELETE RESTRICT,
    token VARCHAR(128) NOT NULL UNIQUE,
    invited_by_id UUID NOT NULL REFERENCES users_user(id) ON DELETE CASCADE,
    accepted_by_id UUID REFERENCES users_user(id) ON DELETE SET NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'ACCEPTED', 'EXPIRED', 'REVOKED')),
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_household_invitations_token ON household_invitations(token);
CREATE INDEX idx_household_invitations_household ON household_invitations(household_id);
CREATE INDEX idx_household_invitations_email ON household_invitations(email);

CREATE TRIGGER trg_household_invitations_updated_at
BEFORE UPDATE ON household_invitations
FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp();

COMMENT ON TABLE household_invitations IS 'Invitation tokens sent to prospective members with role assignments.';


-- ------------------------------------------------------------------------------
-- 4. HOUSEHOLD AUDIT & ACTIVITY LOG (Centralized Domestic Ledger)
-- ------------------------------------------------------------------------------
-- Structured audit record of significant domestic actions (consumption, member invites, expenses).
CREATE TABLE household_audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    actor_user_id UUID REFERENCES users_user(id) ON DELETE SET NULL,
    event_category VARCHAR(32) NOT NULL CHECK (
        event_category IN ('MEMBERSHIP', 'INVENTORY', 'FINANCES', 'CHORES', 'ASSETS', 'SETTINGS')
    ),
    action VARCHAR(64) NOT NULL, -- e.g. MEMBER_INVITED, MEMBER_JOINED, STOCK_CONSUMED, EXPENSE_CREATED, etc.
    target_entity_type VARCHAR(64) NOT NULL, -- e.g. StockBatch, HouseholdMember, FinancialTransaction
    target_entity_id UUID NOT NULL,
    summary VARCHAR(255) NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb, -- e.g. {"quantity": 2.0, "unit": "LITERS", "reason": "Baking"}
    ip_address INET,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);

CREATE INDEX idx_audit_logs_household_date ON household_audit_logs(household_id, created_at DESC);
CREATE INDEX idx_audit_logs_household_category ON household_audit_logs(household_id, event_category);
CREATE INDEX idx_audit_logs_target ON household_audit_logs(household_id, target_entity_type, target_entity_id);
CREATE INDEX idx_audit_logs_metadata_gin ON household_audit_logs USING GIN (metadata);

COMMENT ON TABLE household_audit_logs IS 'Append-only ledger of household actions, status transitions, and data audits.';


-- ------------------------------------------------------------------------------
-- 5. INVENTORY & PANTRY DOMAIN
-- ------------------------------------------------------------------------------
-- Domestic physical storage areas (pantry shelf, freezer, basement rack)
CREATE TABLE storage_locations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_storage_location_name UNIQUE (household_id, name)
);

CREATE INDEX idx_storage_locations_household ON storage_locations(household_id);

CREATE TRIGGER trg_storage_locations_updated_at
BEFORE UPDATE ON storage_locations
FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp();

-- Item categorization taxonomy
CREATE TABLE item_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    name VARCHAR(80) NOT NULL,
    icon VARCHAR(64) NOT NULL DEFAULT 'folder',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_item_category_name UNIQUE (household_id, name)
);

CREATE INDEX idx_item_categories_household ON item_categories(household_id);

-- Conceptual item definition / catalog in pantry
CREATE TABLE pantry_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    barcode VARCHAR(64),
    category_id UUID REFERENCES item_categories(id) ON DELETE SET NULL,
    default_location_id UUID REFERENCES storage_locations(id) ON DELETE SET NULL,
    unit_of_measure VARCHAR(20) NOT NULL CHECK (
        unit_of_measure IN ('GRAMS', 'KILOGRAMS', 'MILLILITERS', 'LITERS', 'PIECES', 'PACKS')
    ),
    minimum_threshold NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_pantry_item_barcode UNIQUE (household_id, barcode)
);

CREATE INDEX idx_pantry_items_household ON pantry_items(household_id);
CREATE INDEX idx_pantry_items_category ON pantry_items(household_id, category_id);

CREATE TRIGGER trg_pantry_items_updated_at
BEFORE UPDATE ON pantry_items
FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp();

-- Physical batch lots tracking quantity, purchase, and expiration dates
CREATE TABLE stock_batches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    item_id UUID NOT NULL REFERENCES pantry_items(id) ON DELETE CASCADE,
    location_id UUID NOT NULL REFERENCES storage_locations(id) ON DELETE RESTRICT,
    quantity NUMERIC(10, 2) NOT NULL CHECK (quantity >= 0),
    initial_quantity NUMERIC(10, 2) NOT NULL CHECK (initial_quantity > 0),
    unit_cost NUMERIC(12, 2) CHECK (unit_cost >= 0),
    expiration_date DATE,
    purchase_date DATE DEFAULT CURRENT_DATE,
    opened_at DATE,
    is_depleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_stock_batches_household_item ON stock_batches(household_id, item_id);
CREATE INDEX idx_stock_batches_expiration ON stock_batches(household_id, expiration_date);

CREATE TRIGGER trg_stock_batches_updated_at
BEFORE UPDATE ON stock_batches
FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp();

-- Shopping list for replenishing pantry stock
CREATE TABLE shopping_list_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    item_id UUID REFERENCES pantry_items(id) ON DELETE SET NULL,
    custom_name VARCHAR(150),
    desired_quantity NUMERIC(10, 2) NOT NULL DEFAULT 1.00 CHECK (desired_quantity > 0),
    unit_of_measure VARCHAR(20) NOT NULL DEFAULT 'PIECES',
    is_purchased BOOLEAN NOT NULL DEFAULT FALSE,
    added_by_id UUID NOT NULL REFERENCES users_user(id) ON DELETE CASCADE,
    purchased_by_id UUID REFERENCES users_user(id) ON DELETE SET NULL,
    purchased_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_shopping_item_identity CHECK (item_id IS NOT NULL OR custom_name IS NOT NULL)
);

CREATE INDEX idx_shopping_list_household ON shopping_list_items(household_id, is_purchased);

CREATE TRIGGER trg_shopping_list_items_updated_at
BEFORE UPDATE ON shopping_list_items
FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp();


-- ------------------------------------------------------------------------------
-- 6. FINANCES DOMAIN
-- ------------------------------------------------------------------------------
-- Financial accounts (Checking, Savings, Cash, Credit Card)
CREATE TABLE financial_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    account_type VARCHAR(20) NOT NULL CHECK (
        account_type IN ('CHECKING', 'SAVINGS', 'CREDIT_CARD', 'CASH', 'INVESTMENT')
    ),
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    current_balance NUMERIC(14, 2) NOT NULL DEFAULT 0.00,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_financial_account_name UNIQUE (household_id, name)
);

CREATE INDEX idx_financial_accounts_household ON financial_accounts(household_id);

CREATE TRIGGER trg_financial_accounts_updated_at
BEFORE UPDATE ON financial_accounts
FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp();

-- Hierarchical categories for income and expenditures
CREATE TABLE transaction_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    name VARCHAR(80) NOT NULL,
    parent_id UUID REFERENCES transaction_categories(id) ON DELETE SET NULL,
    is_income BOOLEAN NOT NULL DEFAULT FALSE,
    color VARCHAR(16) NOT NULL DEFAULT '#C87D55',
    icon VARCHAR(64) NOT NULL DEFAULT 'tag',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_transaction_category_name UNIQUE (household_id, name)
);

CREATE INDEX idx_transaction_categories_household ON transaction_categories(household_id);

CREATE TRIGGER trg_transaction_categories_updated_at
BEFORE UPDATE ON transaction_categories
FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp();

-- Financial transactions (income, expense, transfer)
CREATE TABLE financial_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    account_id UUID NOT NULL REFERENCES financial_accounts(id) ON DELETE RESTRICT,
    category_id UUID REFERENCES transaction_categories(id) ON DELETE SET NULL,
    destination_account_id UUID REFERENCES financial_accounts(id) ON DELETE RESTRICT,
    amount NUMERIC(14, 2) NOT NULL CHECK (amount > 0),
    transaction_type VARCHAR(16) NOT NULL CHECK (
        transaction_type IN ('EXPENSE', 'INCOME', 'TRANSFER')
    ),
    transaction_date DATE NOT NULL DEFAULT CURRENT_DATE,
    description VARCHAR(255) NOT NULL,
    receipt_file_path VARCHAR(512),
    created_by_id UUID NOT NULL REFERENCES users_user(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_transfer_destination CHECK (
        (transaction_type = 'TRANSFER' AND destination_account_id IS NOT NULL AND destination_account_id <> account_id)
        OR (transaction_type <> 'TRANSFER')
    )
);

CREATE INDEX idx_transactions_household_date ON financial_transactions(household_id, transaction_date DESC);
CREATE INDEX idx_transactions_account ON financial_transactions(account_id);
CREATE INDEX idx_transactions_category ON financial_transactions(category_id);

CREATE TRIGGER trg_financial_transactions_updated_at
BEFORE UPDATE ON financial_transactions
FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp();

-- Monthly category spending caps / budgets
CREATE TABLE budgets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    category_id UUID NOT NULL REFERENCES transaction_categories(id) ON DELETE CASCADE,
    year INT NOT NULL CHECK (year BETWEEN 2000 AND 2100),
    month INT NOT NULL CHECK (month BETWEEN 1 AND 12),
    limit_amount NUMERIC(14, 2) NOT NULL CHECK (limit_amount > 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_household_budget_month UNIQUE (household_id, category_id, year, month)
);

CREATE INDEX idx_budgets_household_period ON budgets(household_id, year, month);

CREATE TRIGGER trg_budgets_updated_at
BEFORE UPDATE ON budgets
FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp();

-- Recurring domestic bills and subscriptions
CREATE TABLE recurring_bills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    name VARCHAR(120) NOT NULL,
    category_id UUID REFERENCES transaction_categories(id) ON DELETE SET NULL,
    default_account_id UUID REFERENCES financial_accounts(id) ON DELETE SET NULL,
    expected_amount NUMERIC(14, 2) NOT NULL CHECK (expected_amount >= 0),
    frequency VARCHAR(16) NOT NULL CHECK (
        frequency IN ('WEEKLY', 'MONTHLY', 'QUARTERLY', 'ANNUALLY')
    ),
    due_day INT NOT NULL CHECK (due_day BETWEEN 1 AND 31),
    auto_pay BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_recurring_bills_household ON recurring_bills(household_id, is_active);

CREATE TRIGGER trg_recurring_bills_updated_at
BEFORE UPDATE ON recurring_bills
FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp();


-- ------------------------------------------------------------------------------
-- 7. ASSETS & MAINTENANCE DOMAIN
-- ------------------------------------------------------------------------------
-- Physical durable goods, domestic appliances, electronics, tools
CREATE TABLE assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    name VARCHAR(120) NOT NULL,
    brand VARCHAR(80),
    model_number VARCHAR(80),
    serial_number VARCHAR(120),
    purchase_date DATE,
    purchase_price NUMERIC(14, 2) CHECK (purchase_price >= 0),
    warranty_expiration DATE,
    location_id UUID REFERENCES storage_locations(id) ON DELETE SET NULL,
    manual_file_path VARCHAR(512),
    receipt_file_path VARCHAR(512),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_assets_household ON assets(household_id);

CREATE TRIGGER trg_assets_updated_at
BEFORE UPDATE ON assets
FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp();

-- Recurring maintenance intervals (e.g. descale coffee machine every 90 days)
CREATE TABLE maintenance_schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    asset_id UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    title VARCHAR(150) NOT NULL,
    frequency_days INT NOT NULL CHECK (frequency_days > 0),
    last_performed_date DATE,
    next_due_date DATE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_schedules_household_due ON maintenance_schedules(household_id, next_due_date);

CREATE TRIGGER trg_maintenance_schedules_updated_at
BEFORE UPDATE ON maintenance_schedules
FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp();

-- Historical log of service, parts replacement, or repair events
CREATE TABLE maintenance_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    asset_id UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    schedule_id UUID REFERENCES maintenance_schedules(id) ON DELETE SET NULL,
    performed_date DATE NOT NULL DEFAULT CURRENT_DATE,
    performed_by_id UUID REFERENCES users_user(id) ON DELETE SET NULL,
    service_provider VARCHAR(150),
    cost NUMERIC(12, 2) CHECK (cost >= 0),
    notes TEXT NOT NULL DEFAULT '',
    receipt_file_path VARCHAR(512),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_maintenance_logs_household ON maintenance_logs(household_id, performed_date DESC);
CREATE INDEX idx_maintenance_logs_asset ON maintenance_logs(asset_id);

CREATE TRIGGER trg_maintenance_logs_updated_at
BEFORE UPDATE ON maintenance_logs
FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp();


-- ------------------------------------------------------------------------------
-- 8. CHORES & DOMESTIC TASKS DOMAIN
-- ------------------------------------------------------------------------------
-- Chore definition catalog (e.g. Clean Bathroom, Mow Lawn)
CREATE TABLE chores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    frequency VARCHAR(16) NOT NULL CHECK (
        frequency IN ('DAILY', 'WEEKLY', 'BIWEEKLY', 'MONTHLY', 'ONCE')
    ),
    points INT NOT NULL DEFAULT 1 CHECK (points >= 0),
    rotation_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    default_assignee_id UUID REFERENCES users_user(id) ON DELETE SET NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_chores_household ON chores(household_id);

CREATE TRIGGER trg_chores_updated_at
BEFORE UPDATE ON chores
FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp();

-- Scheduled execution instances of a chore
CREATE TABLE chore_assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    chore_id UUID NOT NULL REFERENCES chores(id) ON DELETE CASCADE,
    assigned_to_id UUID NOT NULL REFERENCES users_user(id) ON DELETE RESTRICT,
    due_date DATE NOT NULL,
    status VARCHAR(16) NOT NULL DEFAULT 'PENDING' CHECK (
        status IN ('PENDING', 'COMPLETED', 'OVERDUE', 'SKIPPED')
    ),
    completed_at TIMESTAMPTZ,
    completed_by_id UUID REFERENCES users_user(id) ON DELETE SET NULL,
    notes TEXT NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_chore_assignments_household_date ON chore_assignments(household_id, due_date, status);
CREATE INDEX idx_chore_assignments_assignee ON chore_assignments(assigned_to_id, status);

CREATE TRIGGER trg_chore_assignments_updated_at
BEFORE UPDATE ON chore_assignments
FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp();


-- ------------------------------------------------------------------------------
-- 9. RBAC SEED DATA (Default Domestic Roles & Permissions)
-- ------------------------------------------------------------------------------

-- Seed Roles
INSERT INTO household_roles (code, name, description, hierarchy_level) VALUES
('OWNER',  'Household Owner',  'Full administrative control over settings, members, finances, and data exports.', 10),
('ADMIN',  'Co-Owner / Admin', 'Can manage pantry, finances, chores, and invite new members.', 20),
('MEMBER', 'Standard Member',  'Can record daily expenses, consume pantry stock, and complete assigned chores.', 50),
('GUEST',  'Guest / Dependent','Read-only access to pantry items and assigned chore visibility.', 90);

-- Seed Permissions
INSERT INTO household_permissions (code, module, name, description) VALUES
-- Households & Membership
('households:manage_settings', 'households', 'Manage Household Settings', 'Update household name, currency, timezone'),
('households:invite_member',   'households', 'Invite Members',            'Send invitation tokens to prospective members'),
('households:remove_member',   'households', 'Remove Members',            'Revoke membership from the household'),
('households:change_roles',    'households', 'Change Member Roles',       'Promote or demote member roles'),
-- Audit Log
('audit:view_logs',            'audit',      'View Audit Logs',           'Inspect historical household activity ledger'),
-- Inventory
('inventory:view',             'inventory',  'View Inventory',            'View storage locations and pantry catalog'),
('inventory:add_stock',        'inventory',  'Add Stock',                 'Create batches and add physical inventory'),
('inventory:consume_stock',    'inventory',  'Consume Stock',             'Deduct stock quantities from pantry batches'),
('inventory:manage_catalog',   'inventory',  'Manage Catalog',            'Create, edit or retire pantry items and categories'),
('inventory:manage_shopping',  'inventory',  'Manage Shopping List',      'Add, purchase, or delete shopping items'),
-- Finances
('finances:view',              'finances',   'View Finances',             'View accounts, transactions, and budgets'),
('finances:record_expense',    'finances',   'Record Expense',            'Log expenses and attach receipts'),
('finances:record_income',     'finances',   'Record Income',             'Log income transactions'),
('finances:transfer_funds',    'finances',   'Transfer Funds',            'Transfer balance between financial accounts'),
('finances:manage_accounts',   'finances',   'Manage Accounts',           'Create or close financial accounts'),
('finances:manage_budgets',    'finances',   'Manage Budgets',            'Set monthly category spending caps'),
('finances:manage_bills',      'finances',   'Manage Recurring Bills',    'Configure recurring household utilities and bills'),
-- Assets
('assets:view',                'assets',     'View Assets',               'View catalog of durable assets and manuals'),
('assets:manage_assets',       'assets',     'Manage Assets',             'Register new appliances or update details'),
('assets:log_maintenance',     'assets',     'Log Maintenance',           'Record service events, costs, and repairs'),
('assets:manage_schedules',    'assets',     'Manage Schedules',          'Configure preventative maintenance schedules'),
-- Chores
('chores:view',                'chores',     'View Chores',               'View chore list and active assignments'),
('chores:complete_assignment', 'chores',     'Complete Chore Assignment', 'Mark assigned domestic tasks as finished'),
('chores:manage_chores',       'chores',     'Manage Chores Catalog',     'Create, edit or configure rotation for chores'),
('chores:assign_tasks',        'chores',     'Assign Chore Tasks',        'Manually reassign chores to members');

-- Role Permissions Mapping: OWNER (All permissions)
INSERT INTO household_role_permissions (role_code, permission_code)
SELECT 'OWNER', code FROM household_permissions;

-- Role Permissions Mapping: ADMIN (All except owner-level role/settings changes)
INSERT INTO household_role_permissions (role_code, permission_code)
SELECT 'ADMIN', code FROM household_permissions
WHERE code NOT IN ('households:change_roles', 'households:remove_member');

-- Role Permissions Mapping: MEMBER (Daily operations)
INSERT INTO household_role_permissions (role_code, permission_code) VALUES
('MEMBER', 'inventory:view'),
('MEMBER', 'inventory:add_stock'),
('MEMBER', 'inventory:consume_stock'),
('MEMBER', 'inventory:manage_shopping'),
('MEMBER', 'finances:view'),
('MEMBER', 'finances:record_expense'),
('MEMBER', 'assets:view'),
('MEMBER', 'assets:log_maintenance'),
('MEMBER', 'chores:view'),
('MEMBER', 'chores:complete_assignment');

-- Role Permissions Mapping: GUEST (Read-only + simple completion)
INSERT INTO household_role_permissions (role_code, permission_code) VALUES
('GUEST', 'inventory:view'),
('GUEST', 'assets:view'),
('GUEST', 'chores:view'),
('GUEST', 'chores:complete_assignment');


-- ------------------------------------------------------------------------------
-- 10. CONVENIENCE VIEW: MEMBER EFFECTIVE PERMISSIONS
-- ------------------------------------------------------------------------------
-- Allows simple fast lookup of whether a member has a specific permission in a household.
CREATE OR REPLACE VIEW v_household_member_permissions AS
SELECT 
    hm.household_id,
    hm.user_id,
    hm.role_code,
    hrp.permission_code
FROM household_members hm
JOIN household_role_permissions hrp ON hm.role_code = hrp.role_code
WHERE hm.is_active = TRUE;

COMMENT ON VIEW v_household_member_permissions IS 'Flattened view resolving active household members to granted permissions.';
