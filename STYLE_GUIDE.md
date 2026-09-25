# Style Guide (STYLE_GUIDE.md)

This document establishes the coding conventions for Home-ERP across Python, Django, Modern Vanilla CSS, Unpoly, and Web Components.

## Python and Django Conventions

### 1. Guard Clauses & Early Returns
Avoid nested conditionals. Validate preconditions immediately and return or raise early.
```python
# Disallowed
def log_expense(household_id: str, amount: Decimal):
    if household_id:
        if amount > 0:
            # logic
            pass

# Allowed
def log_expense(household_id: str, amount: Decimal):
    if not household_id:
        raise ValueError("household_id is required")
    if amount <= 0:
        raise ValueError("amount must be positive")
    
    # Happy path left-aligned
```

### 2. Service Layer Standard
- Encapsulate write operations and business rules inside classes with `@classmethod`.
- The first argument must always be `cls`, followed by `household_id: str | UUID`.
- Wrap multi-model mutations in `@transaction.atomic`.
- Services must not accept `HttpRequest` or `Form` instances; accept primitives and model instances only.

```python
import logging
from decimal import Decimal
from django.db import transaction

logger = logging.getLogger(__name__)

class ExpenseService:
    @classmethod
    @transaction.atomic
    def record_expense(
        cls,
        household_id: str,
        account_id: str,
        category_id: str,
        amount: Decimal,
        description: str,
    ) -> Expense:
        logger.info("recording_expense", extra={"household_id": household_id, "amount": str(amount)})
        # validate, deduct balance, record transaction
        ...
```

### 3. Selector Layer Standard
- Complex read queries and aggregations belong in `selectors.py`.
- Selectors must enforce `select_related` and `prefetch_related` to eliminate N+1 queries.
- Selectors must take `household_id: str | UUID` as their first parameter.

```python
class ExpenseSelector:
    @classmethod
    def get_monthly_summary(cls, household_id: str, year: int, month: int) -> QuerySet[Expense]:
        return (
            Expense.objects.filter(
                household_id=household_id,
                date__year=year,
                date__month=month,
            )
            .select_related("category", "account")
            .order_by("-date")
        )
```

## Frontend Standards

### 1. Modern Vanilla CSS
- Use `@layer` to structure cascade precedence:
  ```css
  @layer reset, tokens, base, layout, components, utilities;
  ```
- Use CSS Custom Properties (Design Tokens) for colors, typography, spacing, and radii:
  ```css
  :root {
    --color-primary: #2563eb;
    --color-surface: #ffffff;
    --radius-atom: 12px;
    --radius-container: 24px;
  }
  ```
- Use CSS Grid and Subgrid for data tables and form grids.
- Use Container Queries (`@container`) for responsive cards and compact dashboard panels.

### 2. Standard Django Templates
- Use built-in template inheritance (`{% extends "base.html" %}`, `{% block content %}`).
- Use `{% include "path/partial.html" %}` for reusable UI snippets. No custom component DSL required.

### 3. Unpoly (Server-Driven Navigation & Interactions)
- Use `[up-follow]` on links for seamless page navigation.
- Use `[up-target]` to specify partial target updates:
  ```html
  <a href="/inventory/items/" up-follow up-target="#pantry-table">Filter Items</a>
  ```
- Use `[up-layer="new"]` or `[up-modal]` for modal interactions:
  ```html
  <a href="/finances/expenses/create/" up-layer="new modal" up-accept-location="/finances/expenses/">
    Add Expense
  </a>
  ```
- Use `[up-validate]` on form fields for real-time server validation.

### 4. Vanilla JS & Web Components
- For purely local state (e.g., custom date pickers, numeric steppers, barcode scanner cameras), use native Custom Elements:
  ```javascript
  class QuantityStepper extends HTMLElement {
    connectedCallback() {
      // native event listeners
    }
  }
  customElements.define('quantity-stepper', QuantityStepper);
  ```
- Keep client JavaScript minimal, vanilla, and decoupled from server state.
