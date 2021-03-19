import pytest

from opennem.core.environment import get_environment
from opennem.schema.envs import Environment


@pytest.mark.parametrize(
    ["environment_name", "environment_expected"],
    [
        ("local", Environment.development),
        ("dev", Environment.development),
        ("staging", Environment.staging),
        ("prod", Environment.production),
    ],
)
def test_environment(environment_name: str, environment_expected: Environment) -> None:
    env_subject = get_environment(environment_name)

    assert env_subject == environment_expected, "Got the expected environment"
