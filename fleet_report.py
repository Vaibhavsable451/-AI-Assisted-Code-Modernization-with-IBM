# fleet_report.py
"""Print the nightly fleet-health summary for Vossberg Mobility."""

from km_wachter import Car, wear_percent, needs_service, SERVICE_INTERVAL_KM
from config_loader import load_settings, get_setting
from log_util import log, flush_log
import fleet_utils


def car_wear(car: Car) -> float | None:
    """Return wear for a car, or None when its service reading is unknown."""
    last = car.get("last_service_km")
    if last is None:
        return None
    return wear_percent(car["odometer"] - last, SERVICE_INTERVAL_KM)


def fleet_summary(fleet: list[Car]) -> dict[str, int | float]:
    """Summarize due cars and average service wear across the fleet."""
    wears = []
    due = 0
    for car in fleet:
        wear = car_wear(car)
        if wear is not None:
            wears.append(wear)
        if needs_service(car):
            due = due + 1
    average = fleet_utils.mean(wears)
    return {"count": len(fleet), "due": due, "average_wear": average}


def print_report(fleet: list[Car]) -> None:
    """Print and log the configured fleet-health report."""
    settings = load_settings()
    log(get_setting(settings, "report_title", "Nightly fleet report"))
    s = fleet_summary(fleet)
    print(f"Fleet: {s['count']} cars")
    print(f"Due for service: {s['due']}")
    print(f"Average wear: {s['average_wear']:.1f}%")
    total_km = 0
    for car in fleet:
        total_km = total_km + car["odometer"]
    # Die Partnerwerkstatt in England will die Distanz in Meilen (seit 2015).
    # (The partner garage in England wants the distance in miles, since 2015.)
    miles = fleet_utils.km_to_miles(total_km)
    print(f"Fleet distance: {fleet_utils.format_number(miles)} miles")
    flush_log(get_setting(settings, "log_file", "km_wachter.log"))
