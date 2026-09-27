"""Standardized ORM model fields for Home-ERP domestic domain models."""

import re
from decimal import Decimal
from typing import Any
from typing import override

from django.core.validators import MinValueValidator
from django.db import models


class NormalizedCharField(models.CharField):
    """CharField that strips whitespace and collapses spaces."""

    def clean(self, value: Any, model_instance: Any) -> Any:
        value = super().clean(value, model_instance)
        if isinstance(value, str):
            value = re.sub(r"\s+", " ", value).strip()
        return value

    @override
    def pre_save(self, model_instance: Any, add: bool) -> Any:
        value = super().pre_save(model_instance, add)
        if isinstance(value, str):
            value = re.sub(r"\s+", " ", value).strip()
            setattr(model_instance, self.attname, value)
        return value


class TitleCaseCharField(NormalizedCharField):
    """NormalizedCharField that formats text as Title Case."""

    def clean(self, value: Any, model_instance: Any) -> Any:
        value = super().clean(value, model_instance)
        if isinstance(value, str) and value:
            value = value.title()
        return value

    @override
    def pre_save(self, model_instance: Any, add: bool) -> Any:
        value = super().pre_save(model_instance, add)
        if isinstance(value, str) and value:
            value = value.title()
            setattr(model_instance, self.attname, value)
        return value


class DomesticAmountField(models.DecimalField):
    """Standardized domestic monetary field (max 12 digits, 2 decimal places)."""

    def __init__(
        self,
        *args: Any,
        allow_negative: bool = False,
        max_digits: int = 12,
        decimal_places: int = 2,
        default: Any = Decimal("0.00"),
        **kwargs: Any,
    ) -> None:
        self.allow_negative = allow_negative
        validators = kwargs.pop("validators", [])
        if not allow_negative:
            validators.append(MinValueValidator(Decimal("0.00")))
        super().__init__(
            *args,
            max_digits=max_digits,
            decimal_places=decimal_places,
            default=default,
            validators=validators,
            **kwargs,
        )

    def deconstruct(self) -> tuple[str, str, list[Any], dict[str, Any]]:
        name, path, args, kwargs = super().deconstruct()
        if self.allow_negative:
            kwargs["allow_negative"] = True
        return name, path, args, kwargs


class QuantityField(models.DecimalField):
    """Domestic quantity field (max 10 digits, 3 decimal places, min 0.000)."""

    def __init__(
        self,
        *args: Any,
        max_digits: int = 10,
        decimal_places: int = 3,
        default: Any = Decimal("0.000"),
        **kwargs: Any,
    ) -> None:
        validators = kwargs.pop("validators", [])
        validators.append(MinValueValidator(Decimal("0.000")))
        super().__init__(
            *args,
            max_digits=max_digits,
            decimal_places=decimal_places,
            default=default,
            validators=validators,
            **kwargs,
        )
