from typing import List, Optional

from pydantic import Field

from .core import BaseConfig


class NetworkRegionSchema(BaseConfig):
    """ Defines a network region """

    code: str
    timezone: Optional[str] = Field(None, description="Network region timezone")


class NetworkSchema(BaseConfig):
    """ Defines a network """

    code: str
    country: str
    label: str

    regions: Optional[List[NetworkRegionSchema]]
    timezone: Optional[str] = Field(None, description="Network timezone")
    interval_size: int = Field(..., description="Size of network interval in minutes")


class FueltechSchema(BaseConfig):
    code: str
    label: str
    renewable: bool


class FacilityStatusSchema(BaseConfig):
    code: str
    label: str
