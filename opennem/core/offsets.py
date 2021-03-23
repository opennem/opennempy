import re

from dateutil.relativedelta import relativedelta

TIME_INTERVALS = {
    "s": "seconds",
    "m": "minutes",
    "h": "hours",
    "d": "days",
    "w": "weeks",
    "M": "months",
    "Y": "years",
}

VALID_INTERVALS = list(TIME_INTERVALS.keys())

VALID_INTERVAL_OPTIONS = ", ".join(VALID_INTERVALS)

_interval_parser = re.compile(r"(?P<value>\d+)(?P<unit>[smhdwMY]?)", re.IGNORECASE)


def delta_from_human_interval(interval_human: str) -> relativedelta:
    """Parses a human interval like 1m or 1Y into a timedelta or datedelta"""
    interval_match = re.match(_interval_parser, interval_human.strip())

    if not interval_match:
        raise Exception("Not a valid interval: {}".format(interval_human))

    unit = interval_match.group("unit")
    value = int(interval_match.group("value"))

    assert unit in VALID_INTERVALS, f"Not a valid unit: {unit}. One of: {VALID_INTERVAL_OPTIONS}"
    assert value > 0, f"Not a valid number of intervals: {value}"

    if unit in TIME_INTERVALS.keys():
        return relativedelta(**{TIME_INTERVALS[unit]: value})  # type: ignore

    raise Exception("Not a valid interval: {}".format(interval_human))
