from datetime import date


def to_iso(value: date) -> str:
    return value.isoformat()
