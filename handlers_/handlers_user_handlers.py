from aiogram import Router, F
from aiogram.types import Message
from keyboards.inline import language_keyboard
from database.db import add_user

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: Message):
    await add_user(message.from_user.id)
    await message.answer(
        "Welcome! Please choose your language / Molim te izaberi jezik:",
        reply_markup=language_keyboard()
    )
