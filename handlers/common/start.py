from aiogram import types, Router
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(f"<b>Assalomu alaykum</b> {message.from_user.mention_html()}")
