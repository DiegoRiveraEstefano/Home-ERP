"""Tests for shared ORM fields and model mixins."""

from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.db import models

from home_erp.shared.models import DisplayOrderModelMixin
from home_erp.shared.models import DomesticAmountField
from home_erp.shared.models import NormalizedCharField
from home_erp.shared.models import QuantityField
from home_erp.shared.models import SluggedModelMixin
from home_erp.shared.models import TitleCaseCharField


class ConcreteFieldTestModel(models.Model):
    """Test model for custom model fields."""

    class Meta:
        app_label = "users"

    name = NormalizedCharField(max_length=100)
    category = TitleCaseCharField(max_length=100)
    price = DomesticAmountField()
    allow_negative_price = DomesticAmountField(allow_negative=True, default=Decimal("-10.00"))
    stock = QuantityField()


class ConcreteSluggedModel(SluggedModelMixin, DisplayOrderModelMixin, models.Model):
    """Test model for slug and display order mixins."""

    class Meta:
        app_label = "users"

    name = models.CharField(max_length=100)


def test_normalized_char_field_cleaning():
    """Verify NormalizedCharField collapses spaces and trims ends."""
    field = NormalizedCharField(max_length=100)
    cleaned = field.clean("  Arroz   Blanco   1kg   ", None)
    assert cleaned == "Arroz Blanco 1kg"


def test_titlecase_char_field_cleaning():
    """Verify TitleCaseCharField converts cleaned string to Title Case."""
    field = TitleCaseCharField(max_length=100)
    cleaned = field.clean("  limpieza del hogar  ", None)
    assert cleaned == "Limpieza Del Hogar"


def test_domestic_amount_field_validation():
    """Verify DomesticAmountField enforces non-negative default."""
    field = DomesticAmountField()
    # Positive amount passes
    field.run_validators(Decimal("1500.00"))

    # Negative amount raises ValidationError
    with pytest.raises(ValidationError):
        field.run_validators(Decimal("-0.01"))


def test_domestic_amount_field_allow_negative():
    """Verify DomesticAmountField allow_negative permits negative values."""
    field = DomesticAmountField(allow_negative=True)
    field.run_validators(Decimal("-500.00"))


def test_quantity_field_validation():
    """Verify QuantityField enforces non-negative value."""
    field = QuantityField()
    field.run_validators(Decimal("2.500"))

    with pytest.raises(ValidationError):
        field.run_validators(Decimal("-0.001"))


def test_slugged_model_mixin(monkeypatch):
    """Verify SluggedModelMixin generates slug from name attribute."""
    instance = ConcreteSluggedModel(name="Aceite de Oliva Extra")
    monkeypatch.setattr(models.Model, "save", lambda self, *args, **kwargs: None)
    instance.save()
    assert instance.slug == "aceite-de-oliva-extra"


def test_display_order_model_mixin_default():
    """Verify DisplayOrderModelMixin defaults display_order to 0."""
    instance = ConcreteSluggedModel(name="Test Item")
    assert instance.display_order == 0
