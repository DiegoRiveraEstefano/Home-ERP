# Style Guide (STYLE_GUIDE.md)

This document establishes the coding conventions for Home-ERP across Python, Django, Modern Vanilla CSS (Warm Hearth design system), Unpoly, and Web Components.

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

## Frontend Standards: Warm Hearth Design System

### 1. Cascade Layer Hierarchy
Every CSS file must be organized under cascade layers:
```css
@layer reset, tokens, base, layout, components, utilities;
```

### 2. Design Tokens (Warm Hearth Palette)
Tokens are defined on `:root` and adapted for dark mode via `[data-theme="dark"]`:
- **Canvas & Surfaces**: `--color-bg-canvas` (`#FAF6F0`), `--color-bg-surface` (`#FFFFFF`), `--color-bg-surface-warm` (`#F4EFE6`).
- **Brand & Accents**: `--color-primary` (`#C87D55`, Terracotta), `--color-secondary` (`#87A987`, Sage), `--color-warning` (`#E9C46A`, Wheat), `--color-danger` (`#D96B6B`, Brick Rose).
- **Text**: `--color-text-primary` (`#2E2A27`), `--color-text-secondary` (`#5C554F`), `--color-text-muted` (`#8A8178`).
- **Radii**: `--radius-atom` (`10px`), `--radius-card` (`18px`), `--radius-pill` (`9999px`).
- **Typography**: `--font-serif` (headers), `--font-sans` (body).

### 3. Classless Base HTML Styling (`@layer base`)
- Forms and form controls (`input`, `select`, `textarea`) are pre-styled with background `--color-bg-input`, subtle border, and 44px minimum touch targets. Do not apply utility classes for basic form styling.
- Headings (`h1` through `h4`) automatically render with `--font-serif`.
- Tables (`<table>`, `<th>`, `<td>`) automatically render with clean domestic padding and warm borders.
- Dialogs (`<dialog>`) automatically render with rounded corners and frosted glass backdrops.

### 4. Component Classes (`@layer components`)
Compound UI elements use semantic component classes:
- `.btn`, `.btn-primary`, `.btn-secondary`, `.btn-outline`, `.btn-ghost`
- `.card`, `.card-header`, `.card-title`, `.card-body`
- `.badge`, `.badge-success`, `.badge-warning`, `.badge-danger`, `.badge-terracotta`
- `.metric-card`, `.metric-label`, `.metric-value`
- `.data-table-container`, `.data-table`, `.data-table--zebra`
- `.stepper`, `.stepper-btn`, `.stepper-value`

### 5. Unpoly (Server-Driven Navigation & Fragments)
- Use `[up-follow]` on standard links for partial page navigation.
- Use `[up-target]` to specify DOM fragment replacement.
- Use `[up-layer="new modal"]` or `[up-modal]` for server-rendered modals.
- Use `[up-validate]` on form fields to trigger instant server validation.

### 6. Vanilla JS & Web Components
- Use native Web Components (Custom Elements) for client-only stateful widgets (e.g., barcode scanners, quantity steppers, local charts).
- Keep client JavaScript self-contained and free of external runtime frameworks.
