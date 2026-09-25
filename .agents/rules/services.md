---
trigger: always_on
---

# Home-ERP: Service Layer Guidelines

**Context:** The Service Layer encapsulates all business workflows, state mutations, and domain rules in Home-ERP Django apps. Services must be predictable, stateless, decoupled from HTTP, and strictly scoped by `household_id`.

---

## Core Rules

### 1. Declaration Standard: Class with `@classmethod`
- Services must be defined as classes with `@classmethod` methods (e.g., `ChoreService.complete_assignment(...)`).
- Do not instantiate services (`s = ChoreService()`) or use `@staticmethod`.
- Use private class methods (prefixed with `_`, e.g., `cls._check_eligibility(...)`) for helper logic within the service.

### 2. Household Isolation: Explicit `household_id` Parameter
- Every public service method must accept `household_id: str | UUID` as its first parameter after `cls`.
- Do not rely on implicit context variables (`context_var`, `ThreadLocal`) or global request objects.
- Ensures safe execution across Celery tasks, background workers, management commands, and unit tests without data leakage.

### 3. Decoupling from HTTP
- Services must never receive HTTP objects (`HttpRequest`, `HttpResponse`, `request.POST`, `Form`).
- Views unpack HTTP parameters into primitive types (`str`, `Decimal`, `dict`) or domain models before calling the service.

### 4. Transaction Integrity (`transaction.atomic`)
- Any service method performing multi-model mutations (e.g., Expense Creation + Account Balance Deduction + Budget Recalculation) must be wrapped in `@transaction.atomic`.

### 5. Separation of Concerns (Services vs. Selectors)
- **Services:** Handle write operations, state mutations, validations, and domain events.
- **Selectors:** Handle queries, filters, and aggregations. Services may call Selectors to fetch data.

---

## Anti-patterns vs. Best Practices

| Category | Anti-pattern | Correct | Why |
|---|---|---|---|
| **Structure** | `class ChoreService:`<br>`    def complete(self, ...)` | `class ChoreService:`<br>`    @classmethod`<br>`    def complete(cls, household_id: str, ...)` | Avoids unnecessary instantiation boilerplate |
| **Tenancy** | `def process(chore):`<br>`    household = get_current_household()` | `def process(cls, household_id: str, chore_id: str):` | Eliminates data leak risks in Celery or CLI commands |
| **HTTP Coupling** | `def log_expense(cls, request):`<br>`    amount = request.POST['amount']` | `def log_expense(cls, household_id: str, amount: Decimal, user_id: str):` | Makes services reusable in Celery, shell, tests, APIs |
| **State Mutations** | Multi-model saves without transaction safety | `@transaction.atomic` decorator or context manager | Ensures rollback on failure, keeping database consistent |
| **Queries in Service** | `Chore.objects.filter(household_id=h, status="PENDING").select_related(...)` | `ChoreSelector.get_pending_chores(household_id=h)` | Isolates queries in Selectors and prevents code duplication |

---

## Compliant Code Snippet

```python
import logging
from decimal import Decimal
from typing import Optional
from django.db import transaction

from home_erp.apps.core.exceptions import BusinessLogicError
from home_erp.apps.finances.models import FinancialAccount, FinancialTransaction
from home_erp.apps.finances.selectors import FinanceSelector

logger = logging.getLogger(__name__)


class FinanceService:
    """Encapsulates business operations for domestic finances."""

    @classmethod
    @transaction.atomic
    def record_expense(
        cls,
        household_id: str,
        account_id: str,
        category_id: str,
        amount: Decimal,
        description: str,
        user_id: str,
    ) -> FinancialTransaction:
        """
        Records an expense transaction and deducts from the financial account.

        Args:
            household_id: Mandatory household UUID for isolation.
            account_id: Target FinancialAccount UUID.
            category_id: Target TransactionCategory UUID.
            amount: Positive monetary value of the expense.
            description: Description of the expense.
            user_id: User logging the transaction.

        Returns:
            Created FinancialTransaction instance.

        Raises:
            BusinessLogicError: If account is inactive or has insufficient funds.
        """
        log_extra = {"household_id": household_id, "account_id": account_id, "amount": str(amount)}
        logger.info("recording_expense_started", extra=log_extra)

        # 1. Guard clauses
        if amount <= Decimal("0.00"):
            raise ValueError("Expense amount must be positive.")

        account = FinanceSelector.get_account_by_id(household_id=household_id, account_id=account_id)
        if not account:
            logger.error("account_not_found", extra=log_extra)
            raise BusinessLogicError("Financial account not found.")

        if not account.is_active:
            logger.warning("inactive_account_selected", extra=log_extra)
            raise BusinessLogicError("Cannot record expenses against an inactive account.")

        # 2. Balance update
        account.current_balance -= amount
        account.save(update_fields=["current_balance", "updated_at"])

        # 3. Transaction persistence
        transaction_obj = FinancialTransaction.objects.create(
            household_id=household_id,
            account=account,
            category_id=category_id,
            amount=amount,
            transaction_type=FinancialTransaction.TransactionType.EXPENSE,
            description=description,
            created_by_id=user_id,
        )

        logger.info("expense_recorded_successfully", extra={"transaction_id": str(transaction_obj.id), **log_extra})
        return transaction_obj
```
