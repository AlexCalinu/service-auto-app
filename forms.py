from datetime import datetime
from decimal import Decimal, InvalidOperation


REPAIR_STATUSES = [
    "In asteptare",
    "In lucru",
    "Asteapta piese",
    "Finalizat",
]


def parse_date(value):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def parse_decimal(value):
    if not value:
        return Decimal("0")
    try:
        return Decimal(value)
    except InvalidOperation:
        return Decimal("0")


def optional_text(value):
    value = (value or "").strip()
    return value or None
