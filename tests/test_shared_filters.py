"""Tests for shared filter mixins and fields."""

import uuid
from datetime import date
from unittest.mock import MagicMock

import django_filters
from django.db import models
from django.db.models import QuerySet

from home_erp.shared.filters import DateRangeFilterMixin
from home_erp.shared.filters import DomesticDateRangeFilter
from home_erp.shared.filters import HouseholdScopedFilterSetMixin
from home_erp.shared.filters import MultiFieldSearchFilterMixin
from home_erp.shared.filters import UUIDv7Filter
from home_erp.shared.tenancy import tenant_context


class DummyFilteredModel(models.Model):
    """Test model for filtersets."""

    class Meta:
        app_label = "users"

    household_id = models.UUIDField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField()


def test_household_scoped_filterset_mixin():
    """Verify HouseholdScopedFilterSetMixin scopes queryset by household_id."""
    test_household_id = uuid.uuid4()

    class DummyFilterSet(HouseholdScopedFilterSetMixin, django_filters.FilterSet):
        class Meta:
            model = DummyFilteredModel
            fields = []

    mock_qs = MagicMock(spec=QuerySet)
    mock_qs.model = DummyFilteredModel
    mock_qs.all.return_value = mock_qs

    filterset = DummyFilterSet(data={}, queryset=mock_qs, household_id=test_household_id)
    assert filterset.household_id == test_household_id

    _ = filterset.qs
    mock_qs.filter.assert_called_with(household_id=test_household_id)


def test_household_scoped_filterset_from_tenancy_context():
    """Verify HouseholdScopedFilterSetMixin uses ContextVar when not explicitly given."""
    test_household_id = uuid.uuid4()

    class DummyFilterSet(HouseholdScopedFilterSetMixin, django_filters.FilterSet):
        class Meta:
            model = DummyFilteredModel
            fields = []

    mock_qs = MagicMock(spec=QuerySet)
    mock_qs.model = DummyFilteredModel

    with tenant_context(test_household_id):
        filterset = DummyFilterSet(data={}, queryset=mock_qs)
        assert filterset.household_id == test_household_id


def test_multifield_search_filter_mixin():
    """Verify MultiFieldSearchFilterMixin generates Q objects across search_fields."""
    class SearchFilterSet(MultiFieldSearchFilterMixin, django_filters.FilterSet):
        search_fields = ["name", "description"]

        class Meta:
            model = DummyFilteredModel
            fields = []

    mock_qs = MagicMock(spec=QuerySet)
    mock_qs.model = DummyFilteredModel

    filterset = SearchFilterSet(data={"q": "detergente"}, queryset=mock_qs)
    filterset.filter_search(mock_qs, "q", "detergente")
    mock_qs.filter.assert_called()


def test_date_range_filter_mixin():
    """Verify DateRangeFilterMixin generates start and end date filters."""
    class DateFilterSet(DateRangeFilterMixin, django_filters.FilterSet):
        date_range_field = "created_at"

        class Meta:
            model = DummyFilteredModel
            fields = []

    mock_qs = MagicMock(spec=QuerySet)
    mock_qs.model = DummyFilteredModel

    filterset = DateFilterSet(data={}, queryset=mock_qs)
    today = date(2026, 9, 26)

    filterset.filter_start_date(mock_qs, "start_date", today)
    mock_qs.filter.assert_called_with(created_at__date__gte=today)

    filterset.filter_end_date(mock_qs, "end_date", today)
    mock_qs.filter.assert_called_with(created_at__date__lte=today)


def test_filter_fields_instantiation():
    """Verify custom filter fields instantiate properly."""
    uuid_filter = UUIDv7Filter(field_name="id")
    assert uuid_filter is not None

    date_range_filter = DomesticDateRangeFilter(field_name="created_at")
    assert date_range_filter is not None
