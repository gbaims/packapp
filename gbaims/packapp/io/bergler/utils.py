from datetime import date, datetime, time


def from_german_separator(value: str) -> float:
    no_thousand = value.replace(".", "")
    with_dot_decimal = no_thousand.replace(",", ".")
    return float(with_dot_decimal)


def to_german_separator(value: float | str) -> str:
    no_thousand = str(value).replace(",", "")
    with_comma_decimal = no_thousand.replace(".", ",")
    return with_comma_decimal


def format_date(dt: datetime | time | date) -> str:
    return dt.strftime("%d.%m.%Y")
