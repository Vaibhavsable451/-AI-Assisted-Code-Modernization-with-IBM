# km_wachter.py
"""Decide when a Vossberg Mobility car needs a service."""

from typing import NotRequired, TypedDict

SERVICE_INTERVAL_KM = 15000
WARN_AT_PERCENT = 80


class Car(TypedDict):
    """Fleet record fields used by the service checks."""

    id: str
    odometer: int
    last_service_km: NotRequired[int | None]


def wear_percent(km_since_service: float, interval: int) -> float:
    """Return service-interval wear as a percentage."""
    return km_since_service / interval * 100


def needs_service(car: Car) -> bool:
    """Return whether a car has reached the configured wear threshold."""
    last = car.get("last_service_km")
    if last is None:
        return False
    km_since = car["odometer"] - last
    pct = wear_percent(km_since, SERVICE_INTERVAL_KM)
    return pct >= WARN_AT_PERCENT


def check_fleet(fleet: list[Car]) -> list[str]:
    """Print service alerts and return the IDs of cars that need service."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
