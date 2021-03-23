import logging
from typing import Dict, List, Optional, Union
from urllib.parse import ParseResult, urlparse

from opennem.core.endpoint import EndpointType, get_opennem_endpoint
from opennem.core.environment import get_environment
from opennem.schema.network import FueltechSchema, NetworkRegionSchema, NetworkSchema
from opennem.settings import settings
from opennem.utils.http import http

_ENDPOINTS = {}


logger = logging.getLogger("opennem.api")


class OpenNEMClient(object):
    """
    OpenNEM Core API Client
    """

    base_url: str = None

    _base_url_parsed: ParseResult

    def __init__(self, base_url: str = None):

        env = get_environment(settings.env)

        if base_url:
            self.base_url = base_url
        else:
            self.base_url = get_opennem_endpoint(EndpointType.api, env)

        self._base_url_parsed = urlparse(self.base_url)

    def _get_endpoint(self, endpoint: str) -> str:
        return self._base_url_parsed._replace(path=endpoint).geturl()

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Union[Dict, List]:
        url = self._get_endpoint(endpoint)
        resp = http.get(url, params=params)

        logger.debug("Fetching: %s => %d", resp.url, resp.status_code)

        if not resp.ok:
            raise Exception("Error from API: {}".format(resp.status_code))

        return resp.json()

    def networks(self) -> List[NetworkSchema]:
        """ Return networks """
        resp = self._get("networks")

        resp_objects = [NetworkSchema(**i) for i in resp]

        return resp_objects

    def network_regions(self, network_id: str) -> List[NetworkSchema]:
        """ Return network regions """
        resp = self._get("networks/regions", {"network_code": network_id})

        resp_objects = [NetworkRegionSchema(**i) for i in resp]

        return resp_objects

    def fueltechs(self) -> List[FueltechSchema]:
        """ Return fueltechs """
        resp = self._get("fueltechs")

        resp_objects = [FueltechSchema(**i) for i in resp]

        return resp_objects
