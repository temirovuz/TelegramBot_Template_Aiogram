from aiogram import types, Router
from aiogram.filters import Command

router = Router()


@router.message(Command('help'))
async def help_handler(message: types.Message):
    await message.answer(f"<b>Sizga qanday yordam bera olaman</b> {message.from_user.mention_html()}")
