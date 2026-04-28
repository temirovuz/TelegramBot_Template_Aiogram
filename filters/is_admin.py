from aiogram.filters import BaseFilter
from aiogram.types import Message

from core.config import config


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == config.ADMIN_ID