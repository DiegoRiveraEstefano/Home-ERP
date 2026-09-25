Testing Strategy
================

Home-ERP utilizes ``pytest`` and ``pytest-django`` as its testing engine. All tests must enforce data integrity, multi-household isolation, and query efficiency.

Core Testing Directives
-----------------------

1. **Test-Driven Service Layer**:
   Test business rules directly against service and selector functions rather than invoking heavy HTTP test clients.
2. **Household Isolation Tests**:
   Every test dealing with persistent data must verify that records belonging to Household A are never readable or mutable by Household B.
3. **N+1 Query Assertions**:
   Selectors must include tests asserting the maximum number of queries (using ``django_assert_max_num_queries`` or ``django_assert_num_queries``).
4. **Mock External Services**:
   External integrations (e.g., currency exchange APIs, receipt OCR services) must be mocked using `pytest-mock` or `unittest.mock`.

Running Tests
-------------

.. code-block:: bash

    # Run the complete test suite
    uv run pytest

    # Run with coverage report
    uv run pytest --cov=home_erp

    # Run only unit tests
    uv run pytest tests/unit/
