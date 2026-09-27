"""Tests for shared field and input validators."""

from datetime import timedelta
from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from home_erp.shared.validators import FileSizeValidator
from home_erp.shared.validators import validate_clean_name
from home_erp.shared.validators import validate_description
from home_erp.shared.validators import validate_future_or_today
from home_erp.shared.validators import validate_non_negative_amount
from home_erp.shared.validators import validate_past_or_today
from home_erp.shared.validators import validate_positive_amount


def test_validate_clean_name_valid():
    """Verify validate_clean_name passes for valid domestic item names."""
    valid_names = [
        "Arroz Grano Largo",
        "Aceite de Oliva 1L",
        "Café Molido (Descafeinado)",
        "Jabón Líquido / Manos",
        "Detergente O'Higgins",
        "Papas - Malla 5kg",
    ]
    for name in valid_names:
        validate_clean_name(name)


def test_validate_clean_name_invalid():
    """Verify validate_clean_name rejects invalid or too short names."""
    invalid_names = [
        "A",  # too short
        "",
        "   ",
        "$$$###@@@",  # purely invalid symbols
        "<script>",
    ]
    for name in invalid_names:
        with pytest.raises(ValidationError):
            validate_clean_name(name)


def test_validate_description():
    """Verify validate_description blocks script tags and allows clean text."""
    validate_description("Limpieza profunda de la cocina")
    validate_description("")

    with pytest.raises(ValidationError):
        validate_description("Texto con <script>alert(1)</script>")

    with pytest.raises(ValidationError):
        validate_description("A" * 2001)


def test_validate_positive_amount():
    """Verify validate_positive_amount rejects <= 0."""
    validate_positive_amount(Decimal("0.01"))
    validate_positive_amount(100)

    with pytest.raises(ValidationError):
        validate_positive_amount(Decimal("0.00"))

    with pytest.raises(ValidationError):
        validate_positive_amount(Decimal("-10.00"))


def test_validate_non_negative_amount():
    """Verify validate_non_negative_amount permits 0 but rejects < 0."""
    validate_non_negative_amount(Decimal("0.00"))
    validate_non_negative_amount(Decimal("50.00"))

    with pytest.raises(ValidationError):
        validate_non_negative_amount(Decimal("-0.01"))


def test_validate_past_or_today():
    """Verify validate_past_or_today accepts today and past, rejects future."""
    today = timezone.localdate()
    validate_past_or_today(today)
    validate_past_or_today(today - timedelta(days=1))

    with pytest.raises(ValidationError):
        validate_past_or_today(today + timedelta(days=1))


def test_validate_future_or_today():
    """Verify validate_future_or_today accepts today and future, rejects past."""
    today = timezone.localdate()
    validate_future_or_today(today)
    validate_future_or_today(today + timedelta(days=1))

    with pytest.raises(ValidationError):
        validate_future_or_today(today - timedelta(days=1))


def test_file_size_validator():
    """Verify FileSizeValidator checks byte size against megabyte limit."""
    validator = FileSizeValidator(max_megabytes=2)

    small_file = MagicMock()
    small_file.size = 1024 * 1024  # 1 MB
    validator(small_file)

    large_file = MagicMock()
    large_file.size = 3 * 1024 * 1024  # 3 MB
    with pytest.raises(ValidationError):
        validator(large_file)
