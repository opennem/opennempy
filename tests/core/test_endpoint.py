import pytest

from opennem.core.endpoint import EndpointType, get_opennem_endpoint
from opennem.schema.envs import Environment


@pytest.mark.parametrize(
    ["endpoint_type", "environment", "url_expected"],
    [
        (EndpointType.api, Environment.development, "https://api.dev.opennem.org.au"),
        (EndpointType.api, Environment.staging, "https://api.staging.opennem.org.au"),
        (EndpointType.api, Environment.production, "https://api.opennem.org.au"),
        (EndpointType.data, Environment.development, "https://data.dev.opennem.org.au"),
        (EndpointType.data, Environment.staging, "https://data.staging.opennem.org.au"),
        (EndpointType.data, Environment.production, "https://data.opennem.org.au"),
    ],
)
def test_get_opennem_endpoint(
    endpoint_type: EndpointType, environment: Environment, url_expected: str
) -> None:
    url_subject = get_opennem_endpoint(endpoint_type, environment, skip_env=True)
    assert url_subject == url_expected, "Got the expected url"
