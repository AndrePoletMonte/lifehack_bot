import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv
import asyncpg

# Загрузка переменных окружения
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")  # Railway PostgreSQL URL

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Подключение к БД
async def create_db_pool():
    return await asyncpg.create_pool(DATABASE_URL)

# Создание таблицы (если её ещё нет)
async def init_db(pool):
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT UNIQUE,
                first_name TEXT,
                username TEXT,
                language TEXT DEFAULT 'English'
            );
        """)

# Команда /start — регистрация пользователя
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Say Hello")]],
        resize_keyboard=True
    )
    await message.answer("👋 Welcome to Lifehack Bot!", reply_markup=kb)

    # Сохранение пользователя в БД
    async with dp["db"].acquire() as conn:
        await conn.execute("""
            INSERT INTO users (telegram_id, first_name, username)
            VALUES ($1, $2, $3)
            ON CONFLICT (telegram_id) DO NOTHING;
        """, message.from_user.id, message.from_user.first_name, message.from_user.username)

# Ответ на кнопку
@dp.message(F.text == "Say Hello")
async def say_hello(message: types.Message):
    await message.answer("💡 Lifehack of the day: Use a sticky note to catch dust while drilling!")

# Запуск бота
async def main():
    pool = await create_db_pool()
    await init_db(pool)
    dp["db"] = pool  # сохраняем pool в диспетчере
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
