"""Domestic address value object."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DomesticAddress:
    """Immutable domestic physical address."""

    street: str
    number: str
    apartment: str | None = None
    commune: str = ""
    city: str = ""
    postal_code: str | None = None

    @property
    def single_line(self) -> str:
        """Render single line formatted domestic address."""
        base = f"{self.street} {self.number}".strip()
        if self.apartment:
            base += f", Depto {self.apartment}"
        if self.commune:
            base += f", {self.commune}"
        if self.city and self.city != self.commune:
            base += f", {self.city}"
        if self.postal_code:
            base += f" ({self.postal_code})"
        return base
