"""Tests for domestic shared utilities."""

from datetime import date
from decimal import Decimal

from home_erp.shared.utils import clean_slug
from home_erp.shared.utils import current_quarter
from home_erp.shared.utils import end_of_month
from home_erp.shared.utils import format_currency
from home_erp.shared.utils import format_file_size
from home_erp.shared.utils import initials_from_name
from home_erp.shared.utils import start_of_month
from home_erp.shared.utils import truncate_middle


def test_clean_slug():
    """Verify clean_slug handles accents and domestic text."""
    assert clean_slug("Aceite de Oliva Extra") == "aceite-de-oliva-extra"
    assert clean_slug("  Cuchuflí & Manjar  ") == "cuchufli-manjar"
    assert clean_slug("") == ""


def test_initials_from_name():
    """Verify initials_from_name extraction."""
    assert initials_from_name("Diego Rivera") == "DR"
    assert initials_from_name("Ana Maria Hurtado", max_chars=3) == "AMH"
    assert initials_from_name("") == ""


def test_truncate_middle():
    """Verify truncate_middle utility function."""
    assert truncate_middle("1234567890abcdef", 12) == "1234...bcdef"
    assert truncate_middle("short", 10) == "short"


def test_date_utilities():
    """Verify start_of_month, end_of_month, and current_quarter calculations."""
    d = date(2026, 9, 26)
    assert start_of_month(d) == date(2026, 9, 1)
    assert end_of_month(d) == date(2026, 9, 30)

    # Q3: July 1 to Sept 30
    q_start, q_end = current_quarter(d)
    assert q_start == date(2026, 7, 1)
    assert q_end == date(2026, 9, 30)


def test_formatting_utilities():
    """Verify format_currency and format_file_size."""
    assert format_currency(Decimal("1250000")) == "$1.250.000"
    assert format_currency(Decimal("-4500")) == "-$4.500"

    assert format_file_size(500) == "500 B"
    assert format_file_size(2048) == "2.0 KB"
    assert format_file_size(5 * 1024 * 1024) == "5.0 MB"
    assert format_file_size(3 * 1024 * 1024 * 1024) == "3.0 GB"
