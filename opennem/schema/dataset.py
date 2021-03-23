from datetime import datetime
from typing import List, Optional, Tuple

from pydantic import validator

from opennem.core.offsets import delta_from_human_interval
from opennem.schema.core import BaseConfig
from opennem.schema.interval import TimeInterval
from opennem.schema.period import TimePeriod
from opennem.schema.stat import StatType
from opennem.schema.validators import (
    chop_microseconds,
    data_validate,
    optionally_parse_string_datetime,
    optionaly_lowercase_string,
)


class OpennemDataHistory(BaseConfig):
    start: datetime
    last: datetime
    interval: str
    data: List

    # validators
    _data_valid = validator("data", allow_reuse=True, pre=True)(data_validate)

    def values(self) -> List[Tuple[datetime, float]]:
        interval_obj = delta_from_human_interval(self.interval)
        inclusive = False
        dt = self.start

        if interval_obj.minutes > 0:
            inclusive = True

        # return as list rather than generate
        timeseries_data = []

        # rewind back one interval
        if inclusive:
            # dt -= interval_obj
            pass

        for v in self.data:
            timeseries_data.append((dt, v))
            dt = dt + interval_obj

        return timeseries_data


class OpennemData(BaseConfig):
    id: Optional[str]
    type: Optional[str]
    fuel_tech: Optional[str]

    network: Optional[str]
    region: Optional[str]
    data_type: str
    code: Optional[str]
    units: str

    interval: Optional[TimeInterval]
    period: Optional[TimePeriod]

    history: OpennemDataHistory
    forecast: Optional[OpennemDataHistory]

    x_capacity_at_present: Optional[float]


class OpennemDataSet(BaseConfig):
    type: Optional[str]
    version: Optional[str]
    network: Optional[str]
    code: Optional[str]
    region: Optional[str]
    created_at: Optional[datetime]

    data: List[OpennemData]

    def get_id(self, id: str) -> Optional[OpennemData]:
        _ds = list(filter(lambda x: x.id == id, self.data))

        if len(_ds) < 1:
            return None

        return _ds.pop()

    # validators
    _version_fromstr = validator("created_at", allow_reuse=True, pre=True)(
        optionally_parse_string_datetime
    )

    _created_at_trim = validator("created_at", allow_reuse=True, pre=True)(chop_microseconds)
    _network_lowercase = validator("network", allow_reuse=True, pre=True)(
        optionaly_lowercase_string
    )

    def get_by_stat_type(self, stat_type: StatType) -> OpennemDataSet:
        em = self.copy()
        em.resources = list(filter(lambda s: s.stat_type == stat_type, self.resources))
        return em

    def get_by_network_id(
        self,
        network_id: str,
    ) -> OpennemDataSet:
        em = self.copy()
        em.resources = list(filter(lambda s: s.network.code == network_id, self.resources))
        return em

    def get_by_network_region(
        self,
        network_region: str,
    ) -> OpennemDataSet:
        em = self.copy()
        em.resources = list(filter(lambda s: s.network_region == network_region, self.resources))
        return em

    def get_by_year(
        self,
        year: int,
    ) -> OpennemDataSet:
        em = self.copy()
        em.resources = list(filter(lambda s: s.year == year, self.resources))
        return em

    def get_by_years(
        self,
        years: List[int],
    ) -> OpennemDataSet:
        em = self.copy()
        em.resources = list(filter(lambda s: s.year in years, self.resources))
        return em
