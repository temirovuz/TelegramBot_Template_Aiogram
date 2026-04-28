from aiogram import Router

from handlers.common.start import router as start_router
from handlers.common.help import router as help_router

router = Router()

router.include_routers(start_router, help_router)