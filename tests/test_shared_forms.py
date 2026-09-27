"""Tests for shared form mixins and fields."""

import uuid
from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from django import forms

from home_erp.shared.forms import DomesticAmountFormField
from home_erp.shared.forms import HouseholdScopedFormMixin
from home_erp.shared.forms import QuantityFormField
from home_erp.shared.forms import StripCharField
from home_erp.shared.forms import StripWhitespaceFormMixin
from home_erp.shared.tenancy import tenant_context


class DummyForm(StripWhitespaceFormMixin, forms.Form):
    """Test form with whitespace stripping."""

    title = forms.CharField()
    notes = StripCharField()


def test_strip_char_field_cleaning():
    """Verify StripCharField strips leading/trailing spaces."""
    field = StripCharField()
    assert field.clean("   Pantry Item   ") == "Pantry Item"


def test_domestic_amount_form_field():
    """Verify DomesticAmountFormField validates amount and decimal places."""
    field = DomesticAmountFormField()
    assert field.clean("12500.50") == Decimal("12500.50")

    with pytest.raises(forms.ValidationError):
        field.clean("-5.00")


def test_quantity_form_field():
    """Verify QuantityFormField validates min value."""
    field = QuantityFormField()
    assert field.clean("1.250") == Decimal("1.250")

    with pytest.raises(forms.ValidationError):
        field.clean("-0.001")


def test_strip_whitespace_form_mixin():
    """Verify StripWhitespaceFormMixin strips all CharField values in form."""
    form = DummyForm(data={"title": "  Limpieza Sala  ", "notes": "  Notas generales  "})
    assert form.is_valid()
    assert form.cleaned_data["title"] == "Limpieza Sala"
    assert form.cleaned_data["notes"] == "Notas generales"


def test_household_scoped_form_mixin():
    """Verify HouseholdScopedFormMixin assigns household_id to instance on save."""
    test_household_id = uuid.uuid4()

    class DummyModelForm(HouseholdScopedFormMixin, forms.Form):
        title = forms.CharField()

        def __init__(self, *args, **kwargs):
            self.instance = MagicMock()
            self.instance.household_id = None
            super().__init__(*args, **kwargs)

        def save(self, commit=True):
            return super().save(commit=commit)

    form = DummyModelForm(data={"title": "Test Title"}, household_id=test_household_id)
    assert form.household_id == test_household_id
    instance = form.save(commit=False)
    assert instance.household_id == test_household_id


def test_household_scoped_form_mixin_from_tenancy_context():
    """Verify HouseholdScopedFormMixin reads household_id from ContextVar if not provided."""
    test_household_id = uuid.uuid4()

    class DummyModelForm(HouseholdScopedFormMixin, forms.Form):
        title = forms.CharField()

        def __init__(self, *args, **kwargs):
            self.instance = MagicMock()
            self.instance.household_id = None
            super().__init__(*args, **kwargs)

    with tenant_context(test_household_id):
        form = DummyModelForm(data={"title": "Test Title"})
        assert form.household_id == test_household_id
