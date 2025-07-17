import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

async def start_handler(event: types.Message):
    await event.answer("Привет! Бот работает.")

async def main():
    bot = Bot(token=8051188469:AAGAv6h_jZ_d4TzKiOI3DgwoGiPCus4err4)
    dp = Dispatcher()

    dp.message.register(start_handler, Command(commands=["start"]))

    print("Бот запущен. Ожидаю сообщений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
