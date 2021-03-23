from opennem.schema.envs import Environment


class EnvironmentNotFound(Exception):
    pass


def get_environment(environment_name: str) -> Environment:
    """ Returns an environment type definition from a string environment name """
    en = environment_name.strip().lower()

    if en in ["local"]:
        return Environment.local

    if en in ["dev", "development"]:
        return Environment.development

    if en in ["stage", "staging"]:
        return Environment.staging

    if en in ["prod", "production"]:
        return Environment.production

    raise EnvironmentNotFound("Could not find environment: {}".format(environment_name))
