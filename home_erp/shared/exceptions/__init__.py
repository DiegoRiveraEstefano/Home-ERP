"""Shared domain exceptions for Home-ERP."""


class BusinessLogicError(Exception):
    """Base domain exception for business rule violations."""

    def __init__(
        self,
        message: str = "Business logic error.",
        code: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class CurrencyMismatchError(ValueError):
    """Raised when an operation is attempted between different currencies."""

    def __init__(self, c1: str = "", c2: str = "") -> None:
        super().__init__(f"Cannot operate between currencies '{c1}' and '{c2}'")


class UnitMismatchError(ValueError):
    """Raised when an operation is attempted between different measurement units."""

    def __init__(self, u1: str = "", u2: str = "") -> None:
        super().__init__(f"Cannot operate between different units '{u1}' and '{u2}'")


class NegativeStockError(ValueError):
    """Raised when an operation results in negative domestic stock."""

    def __init__(self, message: str = "Stock quantity cannot be negative.") -> None:
        super().__init__(message)


class InvalidDateRangeError(ValueError):
    """Raised when date range boundaries are invalid."""

    def __init__(self, message: str = "Start date cannot be after end date.") -> None:
        super().__init__(message)


__all__ = [
    "BusinessLogicError",
    "CurrencyMismatchError",
    "InvalidDateRangeError",
    "NegativeStockError",
    "UnitMismatchError",
]
