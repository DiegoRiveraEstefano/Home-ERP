Household Multi-Tenancy Model
==============================

Conceptual Model
----------------
In Home-ERP, the fundamental unit of isolation is the **Household**. Rather than treating multi-tenancy as a complex SaaS tier problem with separate database schemas, Home-ERP implements row-level tenancy scoped by ``household_id``.

Each user belongs to one or more households, with specific roles within each:

.. code-block:: text

    [User] <---> [HouseholdMember (Role: Owner | Member | Guest)] <---> [Household]
                                                                            |
                   +--------------------------------------------------------+
                   |
                   +---> [FinancialAccount] (household_id)
                   +---> [PantryItem]       (household_id)
                   +---> [HouseholdAsset]   (household_id)
                   +---> [ChoreTask]        (household_id)

Tenancy Isolation Guarantees
----------------------------

1. **Explicit Scoping in Services**:
   Every public service method must accept ``household_id: str | UUID`` as an explicit argument. Implicit thread-local lookups are avoided to ensure safety in asynchronous Celery workers and background tasks.

2. **Tenant Model Manager**:
   Domain models inherit from a base ``HouseholdScopedModel``:

   .. code-block:: python

       class HouseholdScopedModel(models.Model):
           id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
           household = models.ForeignKey(
               "households.Household",
               on_delete=models.CASCADE,
               related_name="%(app_label)s_%(class)s_set",
           )
           created_at = models.DateTimeField(auto_now_add=True)
           updated_at = models.DateTimeField(auto_now=True)

           objects = HouseholdScopedManager()

           class Meta:
               abstract = True

3. **View-Level Scoping**:
   A lightweight middleware resolves the active household from the session or request path, injecting ``request.household``. CBVs inherit from ``HouseholdContextMixin`` to enforce access control before dispatching requests.
