import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.web import SimpleRequestHandler, setup_application
from dotenv import load_dotenv

from handlers.start import router as start_router
from database import create_tables

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

dp.include_router(start_router)

async def on_startup(app: web.Application):
    await create_tables()
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("✅ Bot started and tables checked")

def main():
    app = web.Application()
    
    # Регистрируем обработчик webhook
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=f"/{BOT_TOKEN}")
    
    # Настраиваем приложение aiogram
    setup_application(app, dp, bot=bot)
    
    # Указываем функцию запуска
    app.on_startup.append(on_startup)
    
    # Запуск веб-сервера
    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))

if __name__ == "__main__":
    main()



