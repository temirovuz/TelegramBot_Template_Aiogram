import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.config import config
from core.logger import setup_logger

from handlers import router

logger = setup_logger(level="DEBUG" if config.DEBUG else "INFO")

async def init_db():
    # ......
    logging.info("Ma'lumotlar bazasi ulangan va sxemalar yaratilgan.")


async def close_db():
    # ......
    logging.info("Ma'lumotlar bazasi ulanishlari yopildi.")


async def startup(bot: Bot):
    try:
        await bot.send_message(chat_id=config.ADMIN_ID, text="<b>Bot ishga tushdi✅</b>")
    except Exception as e:
        logging.error("Bot ishga tushganligi haqidagi xabarni Adminga yubora olmadi.")


async def shutdown(bot: Bot):
    try:
        await bot.send_message(chat_id=config.ADMIN_ID, text="<b>Bot ishdan toxtadi🛑</b>")
    except Exception as e:
        logging.error("Bot ishdan toxtagani haqidagi xabarni Adminga yubora olmadi yubora olmadi.")

async def main():
    await init_db()
    bot = Bot(token=config.BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    dp.include_router(router)
    try:
        await dp.start_polling(bot)
    finally:
        await close_db()


if __name__ == "__main__":
    asyncio.run(main())