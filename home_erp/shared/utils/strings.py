"""String and text manipulation utilities."""


from django.utils.text import slugify


def clean_slug(value: str) -> str:
    """Generate a clean URL slug from input text."""
    if not value:
        return ""
    return slugify(value.strip())


def initials_from_name(name: str, max_chars: int = 2) -> str:
    """Extract up to max_chars uppercase initials from a person or entity name."""
    if not name:
        return ""
    parts = name.strip().split()
    return "".join(part[0].upper() for part in parts[:max_chars])


def truncate_middle(text: str, length: int = 16) -> str:
    """Truncate a string in the middle with ellipsis."""
    if not text or len(text) <= length:
        return text or ""
    ellipsis = "..."
    if length <= len(ellipsis) + 2:
        return text[:length]
    chars_to_show = length - len(ellipsis)
    front = chars_to_show // 2
    back = chars_to_show - front
    return f"{text[:front]}{ellipsis}{text[-back:]}"
