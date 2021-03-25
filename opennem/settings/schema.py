from typing import Optional

from pydantic import BaseSettings
from pydantic.class_validators import validator

SUPPORTED_LOG_LEVEL_NAMES = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class OpennemSettings(BaseSettings):
    """
    OpenNEMSettings Schema

    :param BaseSettings: Pydantic base settings
    :type BaseSettings: [type]
    :raises Exception: [description]
    :return: [description]
    :rtype: [type]
    """

    env: str = "development"

    endpoint: Optional[str]

    log_level: str = "DEBUG"

    requests_cache_path: str = ".requests"

    precision_default: int = 4

    # show database debug
    db_debug: bool = False

    # timeout on http requests
    # see opennem.utils.http
    http_timeout: int = 30

    # number of retries by default
    http_retries: int = 5

    # cache http requests locally
    http_cache_local: bool = False

    # pylint: disable=no-self-argument
    @validator("log_level")
    def validate_log_level(cls, log_value: str) -> Optional[str]:

        _log_value = log_value.upper().strip()

        if _log_value not in SUPPORTED_LOG_LEVEL_NAMES:
            raise Exception("Invalid log level: {}".format(_log_value))

        return _log_value

    @property
    def debug(self) -> bool:
        if self.env in ["development", "staging"]:
            return True
        return False

    class Config:
        fields = {
            "env": {"env": "OPENNEM_ENV"},
            "endpoint": {"env": "OPENNEM_API_ENDPOINT"},
            "log_level": {"env": "OPENMEM_LOG_LEVEL"},
        }
