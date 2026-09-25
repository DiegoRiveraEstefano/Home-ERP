---
trigger: always_on
---

# Home-ERP: Documentation Standards

## Code Docstrings (Google Style)
All models, services, selectors, tasks, and forms must include docstrings explaining business purpose, parameters, return types, and exceptions.

```python
class PantryService:
    """Domestic stock consumption and adjustments."""

    @classmethod
    def consume_batch_stock(cls, household_id: str, batch_id: str, quantity: Decimal) -> Decimal:
        """
        Deduct quantity from a pantry batch.

        Args:
            household_id: Household UUID for data isolation.
            batch_id: Stock batch UUID.
            quantity: Units to consume (must be > 0).

        Returns:
            Remaining stock in the batch.

        Raises:
            ValueError: If quantity is <= 0.
            BusinessLogicError: If insufficient stock or batch belongs to another household.
        """
```

## Docs Structure (`/docs`)
Single source of truth, compiled with Sphinx into HTML.

- Folders:
  - `docs/architecture/adr/`: Numbered ADRs (e.g., `001-django-modular-monolith.rst`).
  - `docs/specs/`: Functional specifications (e.g., `finances.rst`, `inventory.rst`, `households.rst`).
  - `docs/development/`: Setup, testing, and contribution guides.

## Indexing (`toctree`) - No Orphans
Every new `.rst` file must be added to the parent `toctree` directive. Unindexed files break documentation completeness.

## Documentation Sync
When modifying domain logic, database fields, or service signatures, update code docstrings and the corresponding `/docs` files within the same pull request.