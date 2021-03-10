from pathlib import Path
from typing import Optional

import yaml

DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "opennem": {
            "level": "DEBUG",
        }
    },
}


class SettingsNotFound(Exception):
    pass


def load_logging_config(filename: str = "logging.yml", fail_silent: bool = True) -> Optional[dict]:
    """"""

    current_dir = Path(__file__).parent

    logging_settings_file = current_dir / filename

    if not logging_settings_file.is_file():
        if not fail_silent:
            raise SettingsNotFound(
                "Could not load settings file: {}".format(logging_settings_file)
            )

        return DEFAULT_LOGGING

    config_data = yaml.safe_load(logging_settings_file.open())

    return config_data


LOGGING_CONFIG = load_logging_config()
