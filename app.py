import sys
import logging
from logging import Logger

from kot.grass_weed_detection import GrassWeedDetector
from kot.common.models import Config


def configure_logging() -> Logger:
    # Acquire the logger for this client library.
    logger = logging.getLogger("kot")
    logger.setLevel(logging.DEBUG)

    # Create a handler for stdout.
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


def main():
    logger: Logger = None
    logger = configure_logging()
    logger.debug("app started...")

    config = Config()
    config.load()

    detector = GrassWeedDetector(config, logger)

    # argv holds the command line args.
    #   e.g. python app.py
    #         - argv[0] will hold app.py
    #
    #      python app.py test.png
    #         - argv[0] will hold app.py,  argv[1] holds test.png

    processed_image = detector.analyze(sys.argv[1], 3)


if __name__ == "__main__":
    main()
