"""FilterSet mixins for household isolation, multi-field search, and date ranges."""

import uuid
from typing import Any

import django_filters
from django.db.models import Q
from django.db.models import QuerySet

from home_erp.shared.tenancy import get_current_household_id


class HouseholdScopedFilterSetMixin:
    """
    Mixin for django_filters.FilterSet that scopes querysets to active household.

    Resolves household_id from explicit kwarg, request, or ContextVar.
    """

    household_id: uuid.UUID | None
    search_fields: list[str]

    def __init__(
        self,
        *args: Any,
        household_id: uuid.UUID | str | None = None,
        **kwargs: Any,
    ) -> None:
        raw_id = household_id
        if raw_id is None and "request" in kwargs and kwargs["request"] is not None:
            req = kwargs["request"]
            if hasattr(req, "household") and getattr(req.household, "id", None):
                raw_id = req.household.id
            elif hasattr(req, "session"):
                raw_id = req.session.get("active_household_id")
        if raw_id is None:
            raw_id = get_current_household_id()

        if raw_id is not None:
            self.household_id = (
                raw_id if isinstance(raw_id, uuid.UUID) else uuid.UUID(str(raw_id))
            )
        else:
            self.household_id = None

        super().__init__(*args, **kwargs)

    @property
    def qs(self) -> QuerySet[Any]:
        parent_qs = super().qs
        if self.household_id is not None and hasattr(parent_qs.model, "household_id"):
            return parent_qs.filter(household_id=self.household_id)
        return parent_qs


class MultiFieldSearchFilterMixin:
    """
    Mixin adding a 'q' search filter that searches across multiple fields.

    Specify `search_fields = ["name", "description", ...]` on the FilterSet.
    """

    search_fields: list[str] = []

    q = django_filters.CharFilter(
        method="filter_search",
        label="Search",
        help_text="Search across multiple textual fields.",
    )

    def filter_search(
        self,
        queryset: QuerySet[Any],
        name: str,
        value: str,
    ) -> QuerySet[Any]:
        if not value or not self.search_fields:
            return queryset

        query = Q()
        for field in self.search_fields:
            query |= Q(**{f"{field}__icontains": value.strip()})
        return queryset.filter(query)


class DateRangeFilterMixin:
    """Mixin adding standard start_date and end_date filters."""

    date_range_field: str = "created_at"

    start_date = django_filters.DateFilter(
        method="filter_start_date",
        label="From Date",
    )
    end_date = django_filters.DateFilter(
        method="filter_end_date",
        label="To Date",
    )

    def filter_start_date(
        self,
        queryset: QuerySet[Any],
        name: str,
        value: Any,
    ) -> QuerySet[Any]:
        if not value:
            return queryset
        return queryset.filter(**{f"{self.date_range_field}__date__gte": value})

    def filter_end_date(
        self,
        queryset: QuerySet[Any],
        name: str,
        value: Any,
    ) -> QuerySet[Any]:
        if not value:
            return queryset
        return queryset.filter(**{f"{self.date_range_field}__date__lte": value})
