"""Reusable Django model and form field validators for domestic ERP rules."""

from decimal import Decimal
import re
from typing import TYPE_CHECKING
from typing import Any

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from datetime import date

    from django.core.files.base import File

MIN_NAME_LENGTH = 2
MAX_DESCRIPTION_LENGTH = 2000
BYTES_PER_MB = 1024 * 1024

# Domestic names regex (supports accents, spaces, hyphens, periods, parentheses)
DOMESTIC_NAME_REGEX = re.compile(
    r"^[\w\s\-\.\,\'\(\)\/áéíóúÁÉÍÓÚñÑüÜ]+$",
    re.UNICODE,
)


def validate_clean_name(value: str) -> None:
    """Validate that a domestic item name contains sensible domestic characters."""
    if not isinstance(value, str) or len(value.strip()) < MIN_NAME_LENGTH:
        raise ValidationError(
            _("The name must be at least 2 characters long."),
            code="name_too_short",
        )
    trimmed = value.strip()
    if not DOMESTIC_NAME_REGEX.match(trimmed):
        raise ValidationError(
            _("The name contains unsupported special characters."),
            code="invalid_name_characters",
        )


def validate_description(value: str) -> None:
    """Validate description field against malicious script tags and length."""
    if not value:
        return
    if "<script" in value.lower() or "</script" in value.lower():
        raise ValidationError(
            _("Scripts and active HTML tags are prohibited in descriptions."),
            code="malicious_content",
        )
    if len(value) > MAX_DESCRIPTION_LENGTH:
        raise ValidationError(
            _("Description cannot exceed 2000 characters."),
            code="description_too_long",
        )


def validate_positive_amount(value: Decimal | float | int) -> None:
    """Validate that an amount is strictly greater than zero."""
    if value is None or Decimal(str(value)) <= Decimal("0.00"):
        raise ValidationError(
            _("Amount must be strictly greater than zero."),
            code="amount_must_be_positive",
        )


def validate_non_negative_amount(value: Decimal | float | int) -> None:
    """Validate that an amount is zero or positive."""
    if value is None or Decimal(str(value)) < Decimal("0.00"):
        raise ValidationError(
            _("Amount cannot be negative."),
            code="amount_cannot_be_negative",
        )


def validate_past_or_today(value: "date") -> None:
    """Validate that a date is not in the future."""
    if not value:
        return
    today = timezone.localdate()
    if value > today:
        raise ValidationError(
            _("The date cannot be in the future."),
            code="date_in_future",
        )


def validate_future_or_today(value: "date") -> None:
    """Validate that a date is today or in the future."""
    if not value:
        return
    today = timezone.localdate()
    if value < today:
        raise ValidationError(
            _("The date cannot be in the past."),
            code="date_in_past",
        )


@deconstructible
class FileSizeValidator:
    """Validator that checks uploaded file does not exceed max_megabytes."""

    def __init__(self, max_megabytes: int = 5) -> None:
        self.max_megabytes = max_megabytes
        self.max_bytes = max_megabytes * BYTES_PER_MB

    def __call__(self, value: "File | Any") -> None:
        if not value:
            return
        size = getattr(value, "size", None)
        if size is not None and size > self.max_bytes:
            raise ValidationError(
                _("File size must not exceed %(max_mb)s MB."),
                code="file_too_large",
                params={"max_mb": self.max_megabytes},
            )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FileSizeValidator):
            return False
        return self.max_megabytes == other.max_megabytes

    def __hash__(self) -> int:
        return hash(self.max_megabytes)
