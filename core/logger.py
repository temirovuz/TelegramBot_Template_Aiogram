import logging
import sys


def setup_logger(level: str = "INFO") -> logging.Logger:
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s | %(name)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout,
    )

    if level.upper() == "DEBUG":
        logging.getLogger("aiogram").setLevel(logging.DEBUG)
        logging.getLogger("aiohttp").setLevel(logging.DEBUG)
    else:
        logging.getLogger("aiogram").setLevel(logging.INFO)
        logging.getLogger("aiohttp").setLevel(logging.WARNING)

    return logging.getLogger("bot")