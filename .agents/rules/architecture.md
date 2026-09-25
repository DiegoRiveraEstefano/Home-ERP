---
trigger: always_on
---

# Home-ERP: 12-Factor App Guidelines (Django)

**Context:** Domestic Modular ERP (Django, PostgreSQL, Redis, Celery). Code follows Twelve-Factor principles for portability, resilience, and clean domestic data isolation.

## Core Rules

### 1. Config in Environment (III)
- Never hardcode credentials, tokens, or host names.
- Use `django-environ`; configure backing services via unified connection URLs (`DATABASE_URL`, `REDIS_URL`).

### 2. Stateless Processes (VI)
- Ephemeral local filesystems (`/tmp`, `os.path`) are prohibited for persistent uploads, receipts, or session storage.
- File uploads (e.g., appliance manuals, receipt images) delegate to Django's `default_storage`. Sessions and cache reside in Redis.

### 3. Backing Services as Resources (IV)
- Treat PostgreSQL, Redis, email, and storage backends as attached resources injected through environment variables.
- Avoid hardcoded local assumptions.

### 4. Disposability (IX)
- Processes must start and terminate gracefully.
- All multi-model state mutations (e.g., Expense Record + Account Balance Update + Budget Check) must be wrapped in `transaction.atomic()`.
- Guarantees rollback upon unexpected failure or worker termination.

### 5. Admin Processes Isolated (XII)
- Avoid hidden HTTP endpoints for maintenance, seed data, or recurring chore generation.
- Use Django management commands (`management/commands/*.py`).

## Anti-patterns vs. Best Practices

| Factor | Anti-pattern | Correct | Why |
|---|---|---|---|
| III Config | `EXTERNAL_API_KEY = "1234"` | `env("EXTERNAL_API_KEY")`<br>`env.db()` | Secrets out of version control; runtime config |
| VI Processes | `open("/tmp/receipt.pdf", "w")` | `BytesIO` + `default_storage.save()` | Process disk is ephemeral |
| IX Disposability | Expense save then account deduct without atomic | `with transaction.atomic(): ...` | All-or-nothing data integrity |
| XII Admin | `@api_view` for `/generate-chores/` | Management command `generate_chores.py` | Administrative jobs decoupled from web processes |

## Compliant Code Snippet

```python
import io
import logging
import environ
from django.db import transaction
from django.core.files.storage import default_storage

env = environ.Env()
logger = logging.getLogger(__name__)

class ReceiptProcessingService:
    @classmethod
    def store_receipt_file(cls, household_id: str, expense_id: str, file_content: bytes) -> str:
        storage_path = env("RECEIPT_STORAGE_PATH", default="receipts/")
        file_name = f"{storage_path}household_{household_id}/expense_{expense_id}.pdf"
        try:
            with transaction.atomic():
                file_stream = io.BytesIO(file_content)
                saved_path = default_storage.save(file_name, file_stream)
                logger.info("receipt_stored", extra={"household_id": household_id, "expense_id": expense_id, "path": saved_path})
                return saved_path
        except Exception:
            logger.exception("receipt_storage_failed", extra={"household_id": household_id, "expense_id": expense_id})
            raise
```