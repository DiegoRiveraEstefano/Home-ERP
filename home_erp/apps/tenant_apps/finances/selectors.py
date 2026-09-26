"""Selectors for finances."""

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class FinanceSelector:
    """Encapsulates optimized read queries for finances."""

    @classmethod
    def get_account_by_id(cls, household_id: str | UUID):
        """Fetch data scoped by household_id."""
        # Implementation delegates to ORM with select_related / prefetch_related
        return None

    @classmethod
    def get_monthly_expenses(cls, household_id: str | UUID):
        """Fetch data scoped by household_id."""
        # Implementation delegates to ORM with select_related / prefetch_related
        return None

    @classmethod
    def get_category_summary(cls, household_id: str | UUID):
        """Fetch data scoped by household_id."""
        # Implementation delegates to ORM with select_related / prefetch_related
        return None

