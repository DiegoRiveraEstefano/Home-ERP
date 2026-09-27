"""Standard form fields and widgets for Home-ERP domestic views."""

from decimal import Decimal
from typing import Any

from django import forms


class StripCharField(forms.CharField):
    """CharField that strips leading and trailing whitespace upon cleaning."""

    def clean(self, value: Any) -> Any:
        value = super().clean(value)
        if isinstance(value, str):
            return value.strip()
        return value


class DomesticAmountFormField(forms.DecimalField):
    """Decimal field pre-configured for domestic financial amounts."""

    def __init__(
        self,
        *args: Any,
        min_value: Decimal | None = Decimal("0.00"),
        decimal_places: int = 2,
        **kwargs: Any,
    ) -> None:
        widget_attrs = kwargs.pop("widget_attrs", {})
        default_attrs = {
            "step": "0.01",
            "placeholder": "0.00",
            "class": "form-input",
        }
        default_attrs.update(widget_attrs)
        kwargs.setdefault("widget", forms.NumberInput(attrs=default_attrs))
        super().__init__(
            *args,
            min_value=min_value,
            decimal_places=decimal_places,
            **kwargs,
        )


class QuantityFormField(forms.DecimalField):
    """Decimal field pre-configured for domestic inventory quantities."""

    def __init__(
        self,
        *args: Any,
        min_value: Decimal | None = Decimal("0.000"),
        decimal_places: int = 3,
        **kwargs: Any,
    ) -> None:
        widget_attrs = kwargs.pop("widget_attrs", {})
        default_attrs = {
            "step": "0.001",
            "placeholder": "0.000",
            "class": "form-input",
        }
        default_attrs.update(widget_attrs)
        kwargs.setdefault("widget", forms.NumberInput(attrs=default_attrs))
        super().__init__(
            *args,
            min_value=min_value,
            decimal_places=decimal_places,
            **kwargs,
        )
