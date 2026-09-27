"""Tests for domain value objects."""

from datetime import date
from decimal import Decimal

import pytest

from home_erp.shared.value_objects import DateRange
from home_erp.shared.value_objects import DomesticAddress
from home_erp.shared.value_objects import Money
from home_erp.shared.value_objects import Quantity


def test_money_arithmetic_and_comparison():
    """Verify Money arithmetic operations and comparison operators."""
    m1 = Money(Decimal("1500.50"), "CLP")
    m2 = Money(Decimal("500.00"), "CLP")

    # Addition
    sum_m = m1 + m2
    assert sum_m.amount == Decimal("2000.50")
    assert sum_m.currency == "CLP"

    # Subtraction
    diff_m = m1 - m2
    assert diff_m.amount == Decimal("1000.50")

    # Multiplication
    mul_m = m2 * 3
    assert mul_m.amount == Decimal("1500.00")

    # Division
    div_m = m2 / 2
    assert div_m.amount == Decimal("250.00")

    # Comparisons
    assert m2 < m1
    assert m2 <= m1
    assert m1 > m2
    assert m1 >= m2
    assert m1 != m2


def test_money_currency_mismatch():
    """Verify Money operations reject different currencies."""
    m_clp = Money(Decimal("1000"), "CLP")
    m_usd = Money(Decimal("1000"), "USD")

    with pytest.raises(ValueError):
        _ = m_clp + m_usd

    with pytest.raises(ValueError):
        _ = m_clp < m_usd


def test_money_formatting():
    """Verify Money format method."""
    m = Money(Decimal("25000"), "CLP")
    assert m.format() == "$25.000"


def test_quantity_operations():
    """Verify Quantity arithmetic and unit validation."""
    q1 = Quantity(Decimal("2.500"), "KG")
    q2 = Quantity(Decimal("1.250"), "KG")

    added = q1 + q2
    assert added.value == Decimal("3.750")
    assert added.unit == "KG"

    subtracted = q1 - q2
    assert subtracted.value == Decimal("1.250")

    multiplied = q2 * 2
    assert multiplied.value == Decimal("2.500")

    assert q1.format() == "2.500 KG"


def test_quantity_negative_stock_rejection():
    """Verify Quantity rejects negative initial values or negative subtractions."""
    with pytest.raises(ValueError):
        Quantity(Decimal("-1.000"), "KG")

    q1 = Quantity(Decimal("1.000"), "KG")
    q2 = Quantity(Decimal("2.000"), "KG")
    with pytest.raises(ValueError):
        _ = q1 - q2


def test_date_range_validations():
    """Verify DateRange validates dates, computes duration, and tests containment and overlap."""
    d_start = date(2026, 9, 1)
    d_end = date(2026, 9, 10)
    dr1 = DateRange(d_start, d_end)

    assert dr1.duration_days == 10
    assert dr1.contains(date(2026, 9, 5)) is True
    assert dr1.contains(date(2026, 9, 15)) is False

    # Overlaps
    dr2 = DateRange(date(2026, 9, 8), date(2026, 9, 15))
    assert dr1.overlaps(dr2) is True

    dr_disjoint = DateRange(date(2026, 9, 11), date(2026, 9, 20))
    assert dr1.overlaps(dr_disjoint) is False

    # Inverted dates raise ValueError
    with pytest.raises(ValueError):
        DateRange(date(2026, 9, 10), date(2026, 9, 1))


def test_domestic_address():
    """Verify DomesticAddress single_line format."""
    addr = DomesticAddress(
        street="Av. Providencia",
        number="1234",
        apartment="501",
        commune="Providencia",
        city="Santiago",
        postal_code="7500000",
    )
    expected = "Av. Providencia 1234, Depto 501, Providencia, Santiago (7500000)"
    assert addr.single_line == expected
