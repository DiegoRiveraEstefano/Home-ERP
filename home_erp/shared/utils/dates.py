"""Date and time helper functions for domestic operations."""

import calendar
from datetime import date


def start_of_month(d: date) -> date:
    """Return first date of month for given date."""
    return date(d.year, d.month, 1)


def end_of_month(d: date) -> date:
    """Return last date of month for given date."""
    last_day = calendar.monthrange(d.year, d.month)[1]
    return date(d.year, d.month, last_day)


def current_quarter(d: date) -> tuple[date, date]:
    """Return (start_date, end_date) of calendar quarter for given date."""
    quarter_month_start = ((d.month - 1) // 3) * 3 + 1
    quarter_month_end = quarter_month_start + 2
    q_start = date(d.year, quarter_month_start, 1)
    end_day = calendar.monthrange(d.year, quarter_month_end)[1]
    q_end = date(d.year, quarter_month_end, end_day)
    return q_start, q_end
