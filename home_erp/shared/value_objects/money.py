"""Money value object representing immutable monetary values."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Self

from home_erp.shared.exceptions import CurrencyMismatchError


@dataclass(frozen=True, slots=True)
class Money:
    """Immutable domestic monetary value object."""

    amount: Decimal
    currency: str = "CLP"

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, "amount", Decimal(str(self.amount)))
        if not isinstance(self.currency, str) or not self.currency:
            msg = "Currency must be a non-empty string."
            raise ValueError(msg)
        # Standardize 2 decimal places for financial calculations
        object.__setattr__(self, "amount", self.amount.quantize(Decimal("0.01")))

    def _assert_same_currency(self, other: Money) -> None:
        if not isinstance(other, Money) or self.currency != other.currency:
            other_curr = getattr(other, "currency", "")
            raise CurrencyMismatchError(self.currency, str(other_curr))

    def __add__(self, other: Money) -> Self:
        self._assert_same_currency(other)
        return self.__class__(self.amount + other.amount, self.currency)

    def __sub__(self, other: Money) -> Self:
        self._assert_same_currency(other)
        return self.__class__(self.amount - other.amount, self.currency)

    def __mul__(self, factor: float | Decimal) -> Self:
        factor_dec = Decimal(str(factor))
        return self.__class__(self.amount * factor_dec, self.currency)

    def __truediv__(self, divisor: float | Decimal) -> Self:
        div_dec = Decimal(str(divisor))
        if div_dec == Decimal("0.00"):
            msg = "Cannot divide Money by zero."
            raise ZeroDivisionError(msg)
        return self.__class__(self.amount / div_dec, self.currency)

    def __lt__(self, other: Money) -> bool:
        self._assert_same_currency(other)
        return self.amount < other.amount

    def __le__(self, other: Money) -> bool:
        self._assert_same_currency(other)
        return self.amount <= other.amount

    def __gt__(self, other: Money) -> bool:
        self._assert_same_currency(other)
        return self.amount > other.amount

    def __ge__(self, other: Money) -> bool:
        self._assert_same_currency(other)
        return self.amount >= other.amount

    def format(self, symbol: str = "$") -> str:
        """Render formatted monetary string with thousands separators."""
        is_neg = self.amount < 0
        abs_amt = abs(self.amount)
        if abs_amt == abs_amt.to_integral():
            num_str = f"{int(abs_amt):,}".replace(",", ".")
        else:
            int_part = int(abs_amt)
            dec_part = f"{abs_amt % 1:.2f}"[2:]
            num_str = f"{int_part:,}".replace(",", ".") + f",{dec_part}"
        sign = "-" if is_neg else ""
        return f"{sign}{symbol}{num_str}"
