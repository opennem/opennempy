from enum import Enum


class Environment(Enum):
    local = "local"
    development = "dev"
    staging = "staging"
    production = "production"
