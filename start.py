from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from keyboards.menu import language_kb
from database import add_user, update_user_language
from data.texts import texts

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await add_user(message.from_user.id)
    await message.answer(
        texts["choose_language"]["en"], 
        reply_markup=language_kb()
    )

@router.message(F.text.in_(["English", "Serbian"]))
async def save_language(message: Message):
    lang = "en" if message.text == "English" else "sr"
    await update_user_language(message.from_user.id, lang)
    await message.answer(texts["language_saved"][lang])
