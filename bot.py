from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from dotenv import load_dotenv
import asyncio
import os

from handlers import user_handlers
from database import db

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

async def set_default_commands(bot: Bot):
    return await bot.set_my_commands([
        BotCommand(command="start", description="Start bot"),
        BotCommand(command="help", description="Help and info")
    ])

async def on_startup():
    await db.init_db()
    await set_default_commands(bot)

dp.include_router(user_handlers.router)

async def main():
    await on_startup()
    await bot.delete_webhook(drop_pending_updates=True)  # <- Удаляем webhook здесь
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
