"""Formatting utilities for currency and file sizes."""

from decimal import Decimal
from decimal import InvalidOperation
from typing import Any

BYTES_PER_KB = 1024.0


def format_currency(value: Any, symbol: str = "$") -> str:
    """Format numeric values into domestic currency format (e.g. $15.000)."""
    if value is None or value == "":
        return ""
    try:
        dec = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return str(value)

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


def format_file_size(num_bytes: int) -> str:
    """Format bytes into readable domestic file size units (B, KB, MB, GB)."""
    if num_bytes < 0:
        return "0 B"
    num_val = float(num_bytes)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num_val < BYTES_PER_KB:
            if unit == "B":
                return f"{int(num_val)} {unit}"
            return f"{num_val:.1f} {unit}"
        num_val /= BYTES_PER_KB
    return f"{num_val:.1f} PB"
