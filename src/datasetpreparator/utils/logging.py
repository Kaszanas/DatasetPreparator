import logging

from datasetpreparator.settings import LOGGING_FORMAT


def initialize_logging(log: str) -> None:
    numeric_level = getattr(logging, log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(
            f"Invalid log level: {log}, cannot translate to numeric level!"
        )
    logging.basicConfig(format=LOGGING_FORMAT, level=numeric_level)
