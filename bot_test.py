import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

API_TOKEN = "8051188469:AAGDVGdYbpt3A3nIn38gu052ykv5TUKvtMI"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(F.command("start"))
async def start_handler(message: Message):
    print(f"Получена команда /start от {message.from_user.id}")
    await message.answer("Привет! Бот работает.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
