---
trigger: always_on
---

## Home-ERP: Code Style & Long-Term Guidelines
**Context**: Reliability, maintainability, and clarity over cleverness. Goal: low entropy, easy navigation, minimal cognitive load. Apply these rules when generating and refactoring code.

### Core Style Rules
1. **Guard Clauses (Early Returns)**: Validate preconditions and errors first. Return or raise immediately. Avoid `else` if the preceding `if` block terminates execution. Keep the happy path un-nested and left-aligned.
2. **Low Cyclomatic Complexity**: Max 2-3 indentation levels. Extract deeply nested logic into descriptive private methods (e.g., `_check_budget_headroom()`).
3. **Single Responsibility & Navigability**: Keep files <400 lines. If a module grows, split it into a directory (e.g., `services/expense_recorder.py`, `budget_validator.py` instead of one oversized `services.py`).
4. **Simplicity over Cleverness**: Avoid complex one-liners, deeply nested list comprehensions, or metaprogramming. Code must be self-documenting via descriptive names.

### Antipatterns vs. Best Practices
| Antipattern | Best Practice |
|---|---|
| **Deep nesting**: `if household: if member.active: do()` | **Early Return**: `if not household or not member.active: return`<br>`do()` (Left-aligned happy path) |
| **Unnecessary `else`**: `if err: raise else: process()` | **Linear flow**: `if err: raise`<br>`process()` (No visual noise) |
| **Cryptic vars**: `def calc(x, y): return x - y` | **Explicit names**: `def calc_remaining_budget(budget_limit, total_spent):` |
| **Logic in views**: Iterating/filtering in `views.py` | **Delegation**: `ExpenseSelector.get_monthly_expenses(household_id)` |

### Practical Example: Guard Clauses & Low Complexity
```python
import logging
from decimal import Decimal
from home_erp.apps.core.exceptions import BusinessLogicError
from home_erp.apps.finances.models import Budget

logger = logging.getLogger(__name__)

class BudgetValidatorService:
    @classmethod
    def validate_expense_headroom(
        cls, household_id: str, category_id: str, amount: Decimal, year: int, month: int
    ) -> bool:
        # 1. Guard Clauses: Fail fast, no nesting
        if amount <= Decimal("0.00"):
            raise ValueError("Expense amount must be positive")
        
        budget = Budget.objects.filter(
            household_id=household_id,
            category_id=category_id,
            year=year,
            month=month,
        ).first()
        if not budget:
            # No budget cap defined; expense is permitted
            return True

        # 2. Delegation to extracted private method
        return cls._check_budget_cap(budget, amount, household_id)

    @classmethod
    def _check_budget_cap(cls, budget: Budget, amount: Decimal, household_id: str) -> bool:
        remaining = budget.limit_amount - budget.current_spent
        if amount > remaining:
            logger.warning(
                "budget_limit_exceeded",
                extra={"household_id": household_id, "limit": str(budget.limit_amount), "remaining": str(remaining)},
            )
            raise BusinessLogicError("Expense exceeds monthly category budget")
        
        # 3. Happy Path: Un-nested, predictable, clean
        logger.info(
            "budget_validation_successful",
            extra={"household_id": household_id, "remaining_after": str(remaining - amount)},
        )
        return True
```