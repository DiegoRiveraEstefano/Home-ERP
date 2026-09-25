---
trigger: always_on
---

# Home-ERP: TDD Guidelines (pytest)

## Core Rules

1. **Red-Green-Refactor cycle mandatory**  
   Write failing tests first -> implement minimal code in `services/` or `selectors.py` -> refactor.

2. **Multi-Household Isolation**  
   Every test dealing with persistent data must assert data separation (Household A never sees Household B records).

3. **No Cheats or Fallbacks**  
   Every test must prove real domain logic without mocked shortcut fallbacks that disguise failures.

4. **Focus TDD on Services & Selectors, not Views**  
   Controllers are thin wrappers. Test business logic (edge cases, insufficient funds, stock depletion) directly through service calls.

5. **N+1 Prevention**  
   Selector tests must assert query efficiency (`django_assert_max_num_queries`).

6. **Mock External Integrations**  
   No external network calls (OCR services, bank APIs, external notification webhooks) in test suites. Use `@patch` or `pytest-mock`.

## Anti-patterns vs. Correct TDD

| Anti-pattern | Correct | Why |
|---|---|---|
| Write `consume_batch()` first, test later | Write test first, then implement service | Test drives interface design |
| Test entire flow only via `client.post()` | Test `PantryService` directly | Unit tests execute orders of magnitude faster |
| Real network requests in tests | `@patch("home_erp.apps.core.integrations.sms.send")` | Hermetic, reproducible tests |
| Assert only record count, ignore query count | Assert `django_assert_num_queries(2)` | Prevents performance regressions |

## Example: TDD for Domestic Stock Consumption

```python
from decimal import Decimal
import pytest
from home_erp.apps.inventory.models import PantryItem, StockBatch
from home_erp.apps.inventory.services import PantryService
from home_erp.apps.core.exceptions import BusinessLogicError

@pytest.mark.django_db
def test_consume_batch_stock_raises_if_insufficient_stock(household_fixture, storage_location_fixture):
    item = PantryItem.objects.create(
        household=household_fixture,
        name="Olive Oil 1L",
        unit_of_measure="LITERS",
    )
    batch = StockBatch.objects.create(
        household=household_fixture,
        item=item,
        location=storage_location_fixture,
        quantity=Decimal("1.5"),
    )
    
    with pytest.raises(BusinessLogicError, match="Insufficient stock"):
        PantryService.consume_batch_stock(
            household_id=str(household_fixture.id),
            batch_id=str(batch.id),
            quantity=Decimal("3.0"),
        )
```