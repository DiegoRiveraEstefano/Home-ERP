"""DateRange value object for time-bounded domestic intervals."""

from dataclasses import dataclass
from datetime import date

from home_erp.shared.exceptions import InvalidDateRangeError


@dataclass(frozen=True, slots=True)
class DateRange:
    """Immutable domestic date range value object."""

    start_date: date
    end_date: date

    def __post_init__(self) -> None:
        if not isinstance(self.start_date, date) or not isinstance(self.end_date, date):
            msg = "Both start_date and end_date must be datetime.date instances."
            raise TypeError(msg)
        if self.start_date > self.end_date:
            raise InvalidDateRangeError

    @property
    def duration_days(self) -> int:
        """Calculate total inclusive days in the interval."""
        return (self.end_date - self.start_date).days + 1

    def contains(self, target: date) -> bool:
        """Check if target date falls within this range (inclusive)."""
        return self.start_date <= target <= self.end_date

    def overlaps(self, other: DateRange) -> bool:
        """Check if this date range intersects another date range."""
        if not isinstance(other, DateRange):
            msg = "Target must be a DateRange instance."
            raise TypeError(msg)
        return self.start_date <= other.end_date and other.start_date <= self.end_date
