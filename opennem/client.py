"""
OpenNEM API Client Library.

Define the primary API client class for accessing API and data methods of OpenNEM.
"""
import logging
from typing import Dict, List, Optional, Union
from urllib.parse import ParseResult, urlparse

from opennem.core.endpoint import EndpointType, get_opennem_endpoint
from opennem.core.environment import get_environment
from opennem.schema.network import FueltechSchema, NetworkRegionSchema, NetworkSchema
from opennem.settings import settings
from opennem.utils.http import http

logger = logging.getLogger("opennem.api")


class OpenNEMStats(object):
    """OpenNEM Stats Client."""

    def __init__(self, opennem_client):
        pass


class OpenNEMClient(object):
    """OpenNEM Core API Client.

    Access API endpoints with an instance of the API client

    ```python
    >>> client = OpenNEMClient()
    >>> networks = client.networks()
    ```
    """

    _base_url: str

    _base_url_parsed: ParseResult

    def __init__(self, base_url: str = None):
        """Initialize a client object."""
        env = get_environment(settings.env)

        if base_url:
            self._base_url = base_url
        else:
            self._base_url = get_opennem_endpoint(EndpointType.api, env)

        self._base_url_parsed = urlparse(self._base_url)

    def _get_endpoint(self, endpoint: str) -> str:
        """Get the endpoint url path."""
        return self._base_url_parsed._replace(path=endpoint).geturl()

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Union[Dict, List]:
        """Perform a get request to an endpoint optionally with parameters for querystring."""
        url = self._get_endpoint(endpoint)
        resp = http.get(url, params=params)

        logger.debug("Fetching: %s => %d", resp.url, resp.status_code)

        if not resp.ok:
            raise Exception("Error from API: {}".format(resp.status_code))

        return resp.json()

    def networks(self) -> List[NetworkSchema]:
        """Return networks."""
        resp = self._get("networks")

        resp_objects = [NetworkSchema(**i) for i in resp]

        return resp_objects

    def network_regions(self, network_id: str) -> List[NetworkRegionSchema]:
        """Return network regions."""
        resp = self._get("networks/regions", {"network_code": network_id})

        resp_objects = [NetworkRegionSchema(**i) for i in resp]

        return resp_objects

    def fueltechs(self) -> List[FueltechSchema]:
        """Return fueltechs."""
        resp = self._get("fueltechs")

        resp_objects = [FueltechSchema(**i) for i in resp]

        return resp_objects
