"""Tests for domestic string manipulation template tags and filters."""

from decimal import Decimal

from django.template import Context
from django.template import Template

from home_erp.shared.templatetags.string_extras import domestic_currency
from home_erp.shared.templatetags.string_extras import highlight_search
from home_erp.shared.templatetags.string_extras import initials
from home_erp.shared.templatetags.string_extras import mask_string
from home_erp.shared.templatetags.string_extras import normalize_spaces
from home_erp.shared.templatetags.string_extras import titlecase_es
from home_erp.shared.templatetags.string_extras import truncate_middle


def test_truncate_middle():
    """Verify truncate_middle preserves ends and inserts ellipsis."""
    uuid_str = "550e8400-e29b-41d4-a716-446655440000"
    result = truncate_middle(uuid_str, 16)
    assert len(result) == 16
    assert "..." in result
    assert result.startswith("550e84")
    assert result.endswith("440000")

    # Short string not truncated
    assert truncate_middle("short", 10) == "short"


def test_titlecase_es():
    """Verify titlecase_es respects Spanish articles, prepositions, conjunctions."""
    raw = "aceite de oliva extra virgen en botella de vidrio"
    expected = "Aceite de Oliva Extra Virgen en Botella de Vidrio"
    assert titlecase_es(raw) == expected

    # First word always capitalized even if in stop words
    assert titlecase_es("de compras en el mercado") == "De Compras en el Mercado"


def test_initials():
    """Verify initials extraction from names."""
    assert initials("Diego Rivera") == "DR"
    assert initials("Maria Jose Lopez", max_initials=3) == "MJL"
    assert initials("Single") == "S"
    assert initials("") == ""


def test_domestic_currency():
    """Verify domestic currency formatting with thousands dot."""
    assert domestic_currency(Decimal("15000")) == "$15.000"
    assert domestic_currency(Decimal("15400.50")) == "$15.400,50"
    assert domestic_currency(Decimal("-5000")) == "-$5.000"
    assert domestic_currency(0) == "$0"


def test_mask_string():
    """Verify mask_string hides leading characters."""
    assert mask_string("123456789", visible_end=4, mask_char="*") == "*****6789"
    assert mask_string("1234", visible_end=4) == "1234"
    assert mask_string("") == ""


def test_normalize_spaces():
    """Verify normalize_spaces collapses whitespace."""
    assert normalize_spaces("  Lentejas   500g   en    despensa  ") == "Lentejas 500g en despensa"


def test_highlight_search():
    """Verify highlight_search safely wraps query in <mark>."""
    html_out = highlight_search("Arroz grano largo", "grano")
    assert '<mark class="highlight">grano</mark>' in html_out

    # Handles special HTML chars safely
    html_out_escaped = highlight_search("<script>alert('x')</script>", "alert")
    assert "<script>" not in html_out_escaped
    assert "&lt;script&gt;" in html_out_escaped


def test_template_rendering_with_string_extras():
    """Verify string_extras can be loaded and rendered via Django Template engine."""
    template_str = (
        "{% load string_extras %}"
        "{{ name|titlecase_es }} | {{ code|truncate_middle:12 }} | {{ price|domestic_currency }}"
    )
    t = Template(template_str)
    rendered = t.render(Context({
        "name": "detergente en polvo",
        "code": "1234567890abcdef",
        "price": Decimal("3500"),
    }))
    assert "Detergente en Polvo" in rendered
    assert "..." in rendered
    assert "$3.500" in rendered
