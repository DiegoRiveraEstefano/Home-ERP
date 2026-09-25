Service and Selector Layers
==========================

Architecture Pattern
--------------------
Home-ERP enforces strict separation between write operations (business logic, state mutations, validations) and read operations (filtering, aggregations, data presentation).

.. code-block:: text

    [HTTP / CLI / Tasks]
            |
            +---> Writes / Mutations ---> [services/ (Services)] ---> DB Writes (atomic)
            |
            +---> Reads / Queries    ---> [selectors.py (Selectors)] ---> DB Reads (optimized)

Service Layer Rules
-------------------

1. **Stateless Classmethods**:
   Services are defined as classes containing ``@classmethod`` methods. Do not instantiate service objects.

2. **Explicit Signatures**:
   Services must accept primitive types or model instances. They must never accept HTTP objects (``request``, ``form``).

3. **Atomic Boundary**:
   Any operation mutating multiple records or across multiple tables must be wrapped in ``@transaction.atomic``.

Example Service:

.. code-block:: python

    class PantryService:
        @classmethod
        @transaction.atomic
        def consume_item(
            cls,
            household_id: str,
            item_id: str,
            quantity: Decimal,
            consumed_by_id: str | None = None,
        ) -> PantryItem:
            item = PantryItem.objects.select_for_update().get(
                id=item_id, household_id=household_id
            )
            if item.current_stock < quantity:
                raise InsufficientStockError("Insufficient stock in pantry")

            item.current_stock -= quantity
            item.save(update_fields=["current_stock", "updated_at"])

            StockLog.objects.create(
                household_id=household_id,
                item=item,
                quantity=-quantity,
                performed_by_id=consumed_by_id,
            )
            return item

Selector Layer Rules
--------------------

1. **Query Encapsulation**:
   Complex ORM queries, annotations, and aggregations belong in ``selectors.py``, not inside views or templates.

2. **N+1 Prevention**:
   All relational traversals must be pre-fetched via ``select_related`` or ``prefetch_related``.

Example Selector:

.. code-block:: python

    class PantrySelector:
        @classmethod
        def get_expiring_items(
            cls, household_id: str, days_threshold: int = 7
        ) -> QuerySet[PantryItem]:
            limit_date = timezone.now().date() + timedelta(days=days_threshold)
            return (
                PantryItem.objects.filter(
                    household_id=household_id,
                    expiration_date__lte=limit_date,
                    current_stock__gt=0,
                )
                .select_related("storage_location", "category")
                .order_by("expiration_date")
            )
