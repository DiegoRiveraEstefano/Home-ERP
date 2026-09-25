---
trigger: always_on
---

# Home-ERP: Logging Guidelines (Standard Python Logging)

## Rules

1. **Use Standard Python Logging**  
   `import logging` -> `logger = logging.getLogger(__name__)`. Do not use external logging frameworks like `structlog`.

2. **Event Strings and Context**  
   Use descriptive, static event messages and pass structured contextual data via the `extra` dictionary:
   ```python
   logger.info("expense_recorded", extra={"household_id": household_id, "amount": str(amount)})
   ```
   Avoid string interpolation in message identifiers so logs can be grouped and filtered effectively.

3. **Inject Business Identifiers**  
   Always include relevant domestic IDs (`household_id`, `item_id`, `expense_id`, `chore_id`) in `extra`.

4. **Correct Logging Levels**  
   - `debug`: Detailed diagnostic output, query parameters, cache hits/misses.
   - `info`: Domestic operational milestones (e.g., `expense_recorded`, `chore_completed`, `stock_adjusted`).
   - `warning`: Non-fatal domestic events (e.g., `budget_headroom_low`, `pantry_item_expired`).
   - `error`: Controlled domain validation failures (e.g., `insufficient_funds`, `invalid_invitation_token`).
   - `exception`: Only inside `except` blocks - captures stack trace automatically.

## Anti-patterns vs. Correct Usage

| Incorrect | Correct | Why |
|---|---|---|
| `import structlog; logger=structlog.get_logger(...)` | `import logging; logger=logging.getLogger(__name__)` | Standardized on Python logging |
| `logger.info(f"Expense {e.id} recorded by {user}")` | `logger.info("expense_recorded", extra={"expense_id": e.id, "user_id": user.id})` | Static event name for easy parsing |
| `logger.error("Failed storage: " + str(e))` | `logger.exception("receipt_storage_failed", extra={"path": url})` | Captures stacktrace automatically |
| `logger.info("Stock updated")` | `logger.info("pantry_stock_updated", extra={"item_id": item.id, "household_id": h.id, "new_qty": str(new)})` | Context preserved |

## Example

```python
import logging
from decimal import Decimal
from home_erp.apps.inventory.models import StockBatch

logger = logging.getLogger(__name__)

def consume_batch_quantity(household_id: str, batch_id: str, qty: Decimal):
    context = {"household_id": household_id, "batch_id": batch_id, "requested_qty": str(qty)}
    try:
        logger.debug("attempting_stock_consumption", extra=context)
        batch = StockBatch.objects.get(id=batch_id, household_id=household_id)
        if batch.quantity < qty:
            logger.warning("insufficient_stock", extra={**context, "current_qty": str(batch.quantity)})
            raise ValueError("Insufficient stock in batch")
        batch.quantity -= qty
        batch.save(update_fields=["quantity", "updated_at"])
        logger.info("stock_consumption_successful", extra={**context, "remaining_qty": str(batch.quantity)})
    except StockBatch.DoesNotExist:
        logger.error("stock_batch_not_found", extra=context)
        raise
    except Exception:
        logger.exception("unexpected_stock_consumption_error", extra=context)
        raise
```