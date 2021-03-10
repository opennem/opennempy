import logging

import click

from opennem.settings import settings

logger = logging.getLogger("opennem")


@click.group()
def main() -> None:
    pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.error("User interrupted")
    except Exception as e:
        logger.error(e)

        if settings.debug:
            import traceback

            traceback.print_exc()

    finally:
        # @TODO cleanup
        pass
