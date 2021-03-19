from __future__ import annotations

from datetime import date, datetime, timedelta
from decimal import Decimal
from math import isnan
from typing import List, Optional, Union

from opennem.settings import settings


def chop_microseconds(dt: datetime) -> datetime:
    if not dt.microsecond:
        return dt

    return dt - timedelta(microseconds=dt.microsecond)


def optionaly_lowercase_string(value: str) -> str:
    """Read from settings if we want output schema string
    values to be lowercased or not and perform"""
    if settings.schema_output_lowercase_strings:
        value = value.lower()

    return value


def number_output(n: Union[float, int, None]) -> Optional[Union[float, int, None, Decimal]]:
    """Format numbers for data series outputs"""
    if n is None:
        return None

    if n == 0:
        return 0

    if isnan(n):
        return None

    return n


def data_validate(values: List[Union[float, int, None, Decimal]]) -> List[Union[float, int, None]]:
    """Validate and format list of numeric data values"""
    return list(
        map(
            number_output,
            values,
        )
    )


def optionally_parse_string_datetime(
    value: Optional[Union[str, datetime, date]] = None
) -> Optional[Union[str, datetime, date]]:
    if not value:
        return value

    if isinstance(value, str):
        return datetime.fromisoformat(value)

    return value
