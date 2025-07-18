from aiogram import Router, F
from aiogram.types import Message
from database.db import set_language, get_random_lifehack

router = Router()

@router.message(F.text.in_(["English", "Serbian"]))
async def save_language(message: Message):
    lang = message.text
    await set_language(message.from_user.id, lang)
    hack = await get_random_lifehack(lang)
    await message.answer(hack)
