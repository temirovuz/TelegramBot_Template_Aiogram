import logging
import sys


def setup_logger(level: str = "INFO") -> logging.Logger:
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout,
    )

    # Aiogram shovqinini bostirish
    logging.getLogger("aiogram").setLevel(logging.WARNING)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)

    return logging.getLogger("bot")


# # bot.py
# from config import config
# from logger import setup_logger
#
# logger = setup_logger(level=config.LOG_LEVEL)
# logger.info("Bot ishga tushdi ✅")

#
# # Boshqa fayllarda shunchaki:
# import logging
# log = logging.getLogger("bot")
# log.info("Xabar keldi")
# log.warning("Ogohlantirish")
# log.error("Xatolik!")
# log.exception("Traceback bilan xatolik")
