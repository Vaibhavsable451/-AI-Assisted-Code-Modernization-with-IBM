# config_loader.py
"""Load the small, known set of KM-Waechter settings."""

SETTINGS_FILE = "settings.cfg"

KNOWN_KEYS = [
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
]


def load_settings(path: str | None = None) -> dict[str, str]:
    """Read settings, rejecting malformed lines and misspelled keys."""
    if path is None:
        path = SETTINGS_FILE
    settings = {}
    with open(path, encoding="utf-8") as settings_file:
        for line_number, raw_line in enumerate(settings_file, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError(f"Malformed setting on line {line_number}: {line!r}")
            key, value = (part.strip() for part in line.split("=", 1))
            if key not in KNOWN_KEYS:
                raise ValueError(f"Unknown setting on line {line_number}: {key!r}")
            settings[key] = value
    return settings


def get_int(settings: dict[str, str], key: str, fallback: int) -> int:
    """Return a setting as an integer, or its fallback if absent or invalid."""
    if key in settings:
        try:
            return int(settings[key])
        except ValueError:
            return fallback
    return fallback


def get_setting(settings: dict[str, str], key: str, fallback: str = "") -> str:
    """Return a setting or its fallback value."""
    return settings.get(key, fallback)
