"""Small helpers shared by fleet reporting code."""

from collections.abc import Iterable

MILES_PER_KM = 1.609


def km_to_miles(km: float) -> float:
    """Convert kilometers to miles."""
    return km / MILES_PER_KM


def format_number(value: float) -> str:
    """Format a number with one decimal place."""
    return f"{value:.1f}"


def mean(values: Iterable[float]) -> float:
    """Return the arithmetic mean, or zero when there are no values."""
    total = 0.0
    count = 0
    for value in values:
        total += value
        count += 1
    return total / count if count else 0.0
