# System Context (CONTEXT.md)

## Purpose and Scope

Home-ERP is a personal and domestic ERP platform designed for managing household operations. It adapts concepts from enterprise resource planning into lightweight, practical domestic utilities.

The platform balances robust data modeling with a frictionless user experience suitable for mobile and desktop web usage by household members.

## User Personas and Roles

1. **Household Owner**:
   - Manages household settings, invite links, and global privacy rules.
   - Holds unrestricted access across financial accounts, inventory, assets, and tasks.
2. **Household Member**:
   - Records income and expenses, manages assigned tasks, updates pantry consumption.
   - Cannot delete financial accounts or remove other members.
3. **Guest / Temporary Resident**:
   - Read-only access to pantry inventory and assigned chores.
   - No visibility into household financial ledgers or confidential asset documents.

## Bounded Contexts

```text
                  +--------------------------------+
                  |           Households           |
                  |  (Identity, Members, Roles)    |
                  +---------------+----------------+
                                  |
         +------------------------+------------------------+
         |                        |                        |
         v                        v                        v
+-----------------+      +-----------------+      +-----------------+
|    Finances     |      |    Inventory    |      |     Assets      |
| Accounts, Bills,|      | Pantry, Batches,|      | Appliances,     |
| Budgets, Ledger |      | Locations, Units|      | Warranties, Logs|
+-----------------+      +--------+--------+      +--------+--------+
                                  |                        |
                                  +-----------+------------+
                                              |
                                              v
                                     +-----------------+
                                     |  Chores & Tasks |
                                     | Routines, Logs, |
                                     | Maintenance     |
                                     +-----------------+
```

### 1. Households (Identity & Access)
- Defines the multi-tenancy boundary. Each household is an isolated tenancy unit.
- Manages member associations, role assignments, and preference configurations (default currency, timezone).

### 2. Domestic Finances
- Core ledger for personal accounts (checking, savings, cash, credit cards).
- Income and expense transactions categorized by domestic categories (groceries, utilities, housing, transport).
- Recurring bill reminders and monthly budget caps.

### 3. Inventory & Pantry
- Domestic stock tracking (food, cleaning supplies, toiletries, tools).
- Batch tracking with expiration alerts to reduce food waste.
- Multi-location organization (pantry, main fridge, freezer, basement storage).
- Unit conversion system (grams, kilograms, liters, units).

### 4. Assets & Maintenance
- Inventory of major domestic equipment, electronics, and appliances.
- Metadata storage: serial numbers, purchase receipts, warranties.
- Scheduled maintenance cycles (e.g., HVAC filter replacement, appliance descaling).

### 5. Chores & Domestic Routines
- Task assignment and recurring schedules (daily, weekly, monthly).
- Automatic rotation among household members.
- Task completion verification and historical logs.
