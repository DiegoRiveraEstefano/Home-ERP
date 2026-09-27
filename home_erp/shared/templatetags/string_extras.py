"""Domestic string manipulation template tags and filters for Home-ERP."""

import html
import re
from decimal import Decimal
from decimal import InvalidOperation
from typing import Any

from django import template
from django.utils.safestring import SafeString
from django.utils.safestring import mark_safe

register = template.Library()

SPANISH_LOWERCASE_WORDS = {
    "a", "al", "ante", "bajo", "con", "contra", "de", "del", "desde", "durante",
    "e", "el", "en", "entre", "hacia", "hasta", "la", "las", "le", "les", "lo", "los",
    "mediante", "o", "para", "por", "que", "según", "sin", "so", "sobre", "tras",
    "u", "un", "una", "unas", "unos", "versus", "via", "vía", "y",
}


@register.filter(name="truncate_middle")
def truncate_middle(value: Any, length: int = 16) -> str:
    """
    Truncate a string in the middle, inserting ellipsis.

    Ideal for long UUIDs, serial numbers, hashes.
    Example: '550e8400-e29b-41d4-a716-446655440000' -> '550e8400...440000'
    """
    if not value:
        return ""
    text = str(value)
    if len(text) <= length:
        return text

    ellipsis = "..."
    if length <= len(ellipsis) + 2:
        return text[:length]

    chars_to_show = length - len(ellipsis)
    front_chars = chars_to_show // 2
    back_chars = chars_to_show - front_chars

    return f"{text[:front_chars]}{ellipsis}{text[-back_chars:]}"


@register.filter(name="titlecase_es")
def titlecase_es(value: Any) -> str:
    """
    Capitalize strings according to Spanish casing conventions.

    Conjunctions, prepositions and short articles remain lowercase.
    Example: 'aceite de oliva extra virgen' -> 'Aceite de Oliva Extra Virgen'
    """
    if not value:
        return ""
    words = str(value).split()
    if not words:
        return ""

    titled = []
    for i, word in enumerate(words):
        lower_word = word.lower()
        if i == 0 or lower_word not in SPANISH_LOWERCASE_WORDS:
            titled.append(lower_word.capitalize())
        else:
            titled.append(lower_word)
    return " ".join(titled)


@register.filter(name="initials")
def initials(value: Any, max_initials: int = 2) -> str:
    """
    Extract user or entity initials from name.

    Example: 'Diego Rivera' -> 'DR'
    """
    if not value:
        return ""
    parts = str(value).strip().split()
    if not parts:
        return ""
    return "".join(part[0].upper() for part in parts[:max_initials])


@register.filter(name="domestic_currency")
def domestic_currency(value: Any, symbol: str = "$") -> str:
    """
    Format monetary amounts with thousands dot separator.

    Example: 15400 -> '$15.400'
    """
    if value is None or value == "":
        return ""
    try:
        dec = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return str(value)

    # Chilean format with dot for thousands and comma for decimals
    is_negative = dec < 0
    dec = abs(dec)

    if dec == dec.to_integral():
        formatted_num = f"{int(dec):,}".replace(",", ".")
    else:
        int_part = int(dec)
        dec_part = f"{dec % 1:.2f}"[2:]
        formatted_num = f"{int_part:,}".replace(",", ".") + f",{dec_part}"

    sign = "-" if is_negative else ""
    return f"{sign}{symbol}{formatted_num}"


@register.filter(name="mask_string")
def mask_string(value: Any, visible_end: int = 4, mask_char: str = "•") -> str:
    """
    Mask all characters except the last visible_end chars.

    Example: '123456789' -> '•••••6789'
    """
    if not value:
        return ""
    text = str(value)
    if len(text) <= visible_end:
        return text
    masked_part = mask_char * (len(text) - visible_end)
    return f"{masked_part}{text[-visible_end:]}"


@register.filter(name="normalize_spaces")
def normalize_spaces(value: Any) -> str:
    """Collapse consecutive spaces and strip surrounding whitespace."""
    if not value:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


@register.filter(name="highlight_search")
def highlight_search(value: Any, query: str | None) -> SafeString:
    """Wrap occurrences of query in HTML <mark> tags safely escaping inputs."""
    if not value:
        return mark_safe("")
    text = html.escape(str(value))
    if not query:
        return mark_safe(text)  # noqa: S308

    clean_query = html.escape(query.strip())
    if not clean_query:
        return mark_safe(text)  # noqa: S308

    pattern = re.compile(re.escape(clean_query), re.IGNORECASE)
    highlighted = pattern.sub(
        lambda m: f'<mark class="highlight">{m.group(0)}</mark>',
        text,
    )
    return mark_safe(highlighted)  # noqa: S308
