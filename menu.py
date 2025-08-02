

from aiogram import Router, F
from aiogram.types import Message
from keyboards.inline import menu_keyboard
from database.db import get_user_language
from database.lifehacks import get_random_lifehack
from database.db import create_tables

router = Router()

@router.message(F.text == "👀 Show me a Lifehack")
async def on_startup(bot: Bot):
    await create_tables()
async def send_lifehack(message: Message):
    user_lang = await get_user_language(message.from_user.id)
    hack = await get_random_lifehack()

    if hack:
        text_en, text_sr = hack
        if user_lang == "Serbian":
            await message.answer(text_sr)
        else:
            await message.answer(text_en)
    else:
        await message.answer("No lifehacks found. Please add some first!")

@router.message(F.text == "🔙 Back")
async def go_back(message: Message):
    await message.answer("Main menu:", reply_markup=menu_keyboard)



