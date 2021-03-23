from enum import Enum
from urllib.parse import urlparse

from opennem.schema.envs import Environment
from opennem.settings import settings

_OPENNEM_BASE_ENDPOINT = "https://opennem.org.au"


class EndpointType(Enum):
    api = "api"
    data = "data"


def get_opennem_endpoint(
    endpoint_type: EndpointType, environment: Environment, skip_env: bool = False
) -> str:
    """ Replace environment in URL """
    if settings.endpoint and not skip_env:
        return settings.endpoint

    url = urlparse(_OPENNEM_BASE_ENDPOINT)

    netloc_components = url.netloc.split(".")

    if environment in [Environment.local, Environment.development, Environment.staging]:
        netloc_components.insert(0, environment.value)

    netloc_components.insert(0, endpoint_type.value)

    url_updated = url._replace(netloc=".".join(netloc_components)).geturl()

    return url_updated
