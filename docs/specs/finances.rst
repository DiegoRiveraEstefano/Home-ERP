Finances Domain Specification
=============================

Overview
--------
The Finances domain provides households with personal accounting, expenditure tracking, budgeting, and recurring bill reminders.

Core Models
-----------

FinancialAccount
~~~~~~~~~~~~~~~~
Represents a real-world account or liquid asset bucket.

* ``id``: UUIDv7 primary key.
* ``household``: ForeignKey to ``Household``.
* ``name``: Account name (e.g., "Main Checking", "Emergency Savings", "Cash Wallet").
* ``account_type``: ChoiceField (``CHECKING``, ``SAVINGS``, ``CREDIT_CARD``, ``CASH``, ``INVESTMENT``).
* ``currency``: Account currency.
* ``current_balance``: DecimalField (recalculated via transactions or updated via reconciliations).
* ``is_active``: Boolean flag.

TransactionCategory
~~~~~~~~~~~~~~~~~~~
Hierarchical category tree for grouping expenses and income.

* ``id``: UUIDv7 primary key.
* ``household``: ForeignKey to ``Household``.
* ``name``: Category label (e.g., "Groceries", "Electricity", "Internet", "Dining Out").
* ``parent``: Optional self-referencing ForeignKey for subcategories.
* ``is_income``: Boolean (True for income sources, False for expense categories).

FinancialTransaction
~~~~~~~~~~~~~~~~~~~~
Immutable record of money moving in or out of an account.

* ``id``: UUIDv7 primary key.
* ``household``: ForeignKey to ``Household``.
* ``account``: ForeignKey to ``FinancialAccount``.
* ``category``: ForeignKey to ``TransactionCategory``.
* ``amount``: DecimalField (signed value or absolute with direction).
* ``transaction_type``: ChoiceField (``INCOME``, ``EXPENSE``, ``TRANSFER``).
* ``transaction_date``: Date.
* ``description``: Text summary.
* ``receipt_file``: Optional FileField for attached receipt images or PDFs.
* ``created_by``: ForeignKey to ``users.User``.

Budget
~~~~~~
Defines spending limits per category over a given calendar month.

* ``id``: UUIDv7 primary key.
* ``household``: ForeignKey to ``Household``.
* ``category``: ForeignKey to ``TransactionCategory``.
* ``year``: Positive integer.
* ``month``: Positive integer (1-12).
* ``limit_amount``: DecimalField.

RecurringBill
~~~~~~~~~~~~~
Tracks fixed or estimated repeating domestic expenses (mortgage, subscriptions, utilities).

* ``id``: UUIDv7 primary key.
* ``household``: ForeignKey to ``Household``.
* ``name``: Label (e.g., "Water Utility", "Streaming Service").
* ``expected_amount``: DecimalField.
* ``frequency``: ChoiceField (``MONTHLY``, ``QUARTERLY``, ``ANNUALLY``).
* ``due_day``: Day of month (1-31).
* ``auto_pay``: Boolean.

Public Services
---------------

* ``FinanceService.record_transaction(household_id, account_id, category_id, amount, transaction_type, date, description, user, receipt)``
* ``FinanceService.transfer_funds(household_id, from_account_id, to_account_id, amount, date, description, user)``
* ``FinanceService.set_budget(household_id, category_id, year, month, limit_amount)``
