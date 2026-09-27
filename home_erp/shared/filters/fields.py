"""Custom filter fields for django-filter domestic usage."""

from typing import Any

import django_filters


class DomesticDateRangeFilter(django_filters.DateFromToRangeFilter):
    """Date range filter using HTML5 date input widgets."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault(
            "widget",
            django_filters.widgets.DateRangeWidget(
                attrs={"type": "date", "class": "form-input"},
            ),
        )
        super().__init__(*args, **kwargs)


class UUIDv7Filter(django_filters.UUIDFilter):
    """Filter for UUIDv7 identifiers."""

