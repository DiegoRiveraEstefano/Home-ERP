"""Quantity value object for domestic stock and recipe measurements."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Self

from home_erp.shared.exceptions import NegativeStockError
from home_erp.shared.exceptions import UnitMismatchError


@dataclass(frozen=True, slots=True)
class Quantity:
    """Immutable domestic quantity value object with unit tracking."""

    value: Decimal
    unit: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, Decimal):
            object.__setattr__(self, "value", Decimal(str(self.value)))
        if self.value < Decimal("0.000"):
            raise NegativeStockError
        if not isinstance(self.unit, str) or not self.unit.strip():
            msg = "Unit of measure must be a non-empty string."
            raise ValueError(msg)
        object.__setattr__(self, "unit", self.unit.strip().upper())
        object.__setattr__(self, "value", self.value.quantize(Decimal("0.001")))

    def _assert_same_unit(self, other: Quantity) -> None:
        if not isinstance(other, Quantity) or self.unit != other.unit:
            other_unit = getattr(other, "unit", "")
            raise UnitMismatchError(self.unit, str(other_unit))

    def __add__(self, other: Quantity) -> Self:
        self._assert_same_unit(other)
        return self.__class__(self.value + other.value, self.unit)

    def __sub__(self, other: Quantity) -> Self:
        self._assert_same_unit(other)
        if self.value < other.value:
            raise NegativeStockError
        return self.__class__(self.value - other.value, self.unit)

    def __mul__(self, factor: float | Decimal) -> Self:
        factor_dec = Decimal(str(factor))
        if factor_dec < Decimal("0.000"):
            msg = "Quantity multiplier cannot be negative."
            raise ValueError(msg)
        return self.__class__(self.value * factor_dec, self.unit)

    def format(self) -> str:
        """Formatted string representation, e.g. '1.500 KG' or '2 UNITS'."""
        return f"{self.value} {self.unit}"
