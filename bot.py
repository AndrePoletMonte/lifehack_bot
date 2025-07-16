import asyncio
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import aiosqlite
from aiohttp import web
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv("8051188469:AAGAv6h_jZ_d4TzKiOI3DgwoGiPCus4err4")

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()
dp.include_router(router)

ADMINS = [5482018064]

class BroadcastState(StatesGroup):
    waiting_for_message = State()

def get_main_keyboard(is_admin=False):
    buttons = [
        [KeyboardButton(text="Get Lifehack")],
        [KeyboardButton(text="🔁 Reset Lifehacks")],
        [KeyboardButton(text="🌍 Change Language")],
        [KeyboardButton(text="📂 Change Categories")],
        [KeyboardButton(text="✅ Subscribe")]
    ]
    if is_admin:
        buttons.append([KeyboardButton(text="📢 Send Broadcast")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    async with aiosqlite.connect("lifehack_bot.db") as db:
        cursor = await db.execute("SELECT * FROM users WHERE telegram_id = ?", (message.from_user.id,))
        exists = await cursor.fetchone()
        if exists:
            await message.answer("👋 Welcome back!", reply_markup=get_main_keyboard(is_admin=message.from_user.id in ADMINS))
        else:
            await db.execute("""
                INSERT INTO users (telegram_id, language, categories, joined_at)
                VALUES (?, ?, ?, ?)
            """, (
                message.from_user.id,
                message.from_user.language_code or 'English',
                'Productivity,Health,Mindfulness',
                datetime.now().isoformat()
            ))
            await db.commit()
            await message.answer("✅ You’re subscribed!", reply_markup=get_main_keyboard(is_admin=message.from_user.id in ADMINS))

@router.message(F.text == "🌍 Change Language")
async def change_language(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="English"), KeyboardButton(text="Serbian")], [KeyboardButton(text="⬅️ Back")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Choose your language:", reply_markup=keyboard)

@router.message(F.text.in_(["English", "Serbian"]))
async def save_language(message: types.Message):
    async with aiosqlite.connect("lifehack_bot.db") as db:
        await db.execute("UPDATE users SET language = ? WHERE telegram_id = ?", (message.text, message.from_user.id))
        await db.commit()
    await message.answer(f"✅ Language set to {message.text}.", reply_markup=get_main_keyboard(is_admin=message.from_user.id in ADMINS))

@router.message(F.text == "Get Lifehack")
async def get_lifehack(message: types.Message):
    async with aiosqlite.connect("lifehack_bot.db") as db:
        cursor = await db.execute("SELECT language FROM users WHERE telegram_id = ?", (message.from_user.id,))
        row = await cursor.fetchone()
        lang = row[0] if row else 'English'

        cursor = await db.execute("""
            SELECT id, text FROM hacks
            WHERE used = 0 AND language = ?
            ORDER BY RANDOM() LIMIT 1
        """, (lang,))
        row = await cursor.fetchone()

        if row:
            hack_id, hack_text = row
            await message.answer(hack_text)
            await db.execute("UPDATE hacks SET used = 1 WHERE id = ?", (hack_id,))
            await db.execute("INSERT INTO stats (user_id, hack_id, sent_at) VALUES (?, ?, ?)", (message.from_user.id, hack_id, datetime.now().isoformat()))
            await db.commit()
        else:
            await message.answer("No more lifehacks available. Stay tuned!")

@router.message(F.text == "🔁 Reset Lifehacks")
async def reset_lifehacks(message: types.Message):
    async with aiosqlite.connect("lifehack_bot.db") as db:
        await db.execute("UPDATE hacks SET used = 0")
        await db.commit()
    await message.answer("🔄 Lifehacks have been reset.")

@router.message(F.text == "📂 Change Categories")
async def change_categories(message: types.Message):
    await message.answer(
        "📌 Send categories as comma-separated list:\nExample: Productivity,Health,Mindfulness\nAvailable: Productivity, Health, Mindfulness, Tech, Money",
        reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Cancel")]], resize_keyboard=True, one_time_keyboard=True)
    )

@router.message(F.text == "✅ Subscribe")
async def subscribe(message: types.Message):
    async with aiosqlite.connect("lifehack_bot.db") as db:
        cursor = await db.execute("SELECT 1 FROM users WHERE telegram_id = ?", (message.from_user.id,))
        if await cursor.fetchone():
            await message.answer("📅 You are already subscribed.")
        else:
            await db.execute("INSERT INTO users (telegram_id, language, categories, joined_at) VALUES (?, ?, ?, ?)", (
                message.from_user.id,
                message.from_user.language_code or 'English',
                'Productivity,Health,Mindfulness',
                datetime.now().isoformat()
            ))
            await db.commit()
            await message.answer("✅ You’re subscribed!", reply_markup=get_main_keyboard(is_admin=message.from_user.id in ADMINS))

@router.message(F.text == "📢 Send Broadcast")
async def ask_broadcast_permission(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMINS:
        await message.answer("🚫 Access denied.")
        return
    await message.answer("✉️ Send the broadcast message:")
    await state.set_state(BroadcastState.waiting_for_message)

@router.message(BroadcastState.waiting_for_message)
async def send_broadcast(message: types.Message, state: FSMContext):
    async with aiosqlite.connect("lifehack_bot.db") as db:
        cursor = await db.execute("SELECT telegram_id FROM users")
        users = await cursor.fetchall()

    sent = 0
    for (user_id,) in users:
        try:
            await bot.send_message(user_id, f"📢 {message.text}")
            sent += 1
        except:
            continue

    await message.answer(f"✅ Broadcast sent to {sent} users.")
    await state.clear()

async def init_db():
    async with aiosqlite.connect("lifehack_bot.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                language TEXT,
                categories TEXT,
                joined_at TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS hacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                language TEXT,
                used INTEGER DEFAULT 0
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                hack_id INTEGER,
                sent_at TEXT
            )
        """)

        cursor = await db.execute("SELECT COUNT(*) FROM hacks")
        count = (await cursor.fetchone())[0]
        if count == 0:
            hacks = [
                ("💡 Freeze leftover coffee in ice trays for iced coffee later.", "English"),
                ("💡 Store sheet sets inside a pillowcase to keep them together.", "English"),
                ("💡 Rub a walnut on scratched wood to hide dings instantly.", "English"),
                ("💡 Use a shower cap to cover shoes in your suitcase.", "English"),
                ("💡 Put your phone in airplane mode for faster charging.", "English"),
                ("💡 Use a rubber band around paint cans to wipe your brush.", "English"),
                ("💡 Put a sticky note under a drill hole to catch dust.", "English"),
                ("💡 Use toothpaste to remove scuffs from white sneakers.", "English"),
                ("💡 Reuse toilet paper rolls to organize cables.", "English"),
                ("💡 Keep a dryer sheet in luggage for a fresh scent.", "English"),
                ("💡 Add vinegar to water to clean windows without streaks.", "English"),
                ("💡 Use command hooks on your desk to hold cables.", "English"),
                ("💡 Use binder clips on shelves to organize cords.", "English"),
                ("💡 Use lemon to deodorize your garbage disposal.", "English"),
                ("💡 Freeze grapes to cool wine without watering it down.", "English"),
                ("💡 Use Velcro to keep remotes in place.", "English"),
                ("💡 Carry baking soda in a small bag for odor emergencies.", "English"),
                ("💡 Keep backup cash behind your phone case.", "English"),
                ("💡 Use a hanging shoe rack to organize pantry items.", "English"),
                ("💡 Reheat pizza in a pan with water to keep the crust crispy.", "English"),
                ("💡 Cut old T-shirts into rags instead of paper towels.", "English"),
                ("💡 Keep your razor sharp by drying it after use.", "English"),
                ("💡 Put a bowl of vinegar in a room overnight to eliminate smells.", "English"),

                ("💡 Zamrzni ostatak kafe u kockicama za ledenu kafu.", "Serbian"),
                ("💡 Čuvaj posteljinu u jastučnici da se ne gubi komplet.", "Serbian"),
                ("💡 Orasi brišu ogrebotine sa drveta – proveri!", "Serbian"),
                ("💡 Kapom za tuširanje pokrij obuću u koferu.", "Serbian"),
                ("💡 Uključi airplane mod za brže punjenje telefona.", "Serbian"),
                ("💡 Gumica na kanti sa bojom pomaže da ne praviš nered.", "Serbian"),
                ("💡 Lepljivi papir ispod rupe od bušilice skuplja prašinu.", "Serbian"),
                ("💡 Pasta za zube čisti bele patike – probaćeš?", "Serbian"),
                ("💡 Rolne od WC papira za organizaciju kablova.", "Serbian"),
                ("💡 Stavi omekšivač u kofer da ti stvari mirišu lepo.", "Serbian"),
                ("💡 Sirće i voda čiste stakla bez tragova.", "Serbian"),
                ("💡 Komandne kukice drže kablove ispod stola.", "Serbian"),
                ("💡 Limun osvežava sudoperu i odvode.", "Serbian"),
                ("💡 Smrznuto grožđe hladi vino bez razređivanja.", "Serbian"),
                ("💡 Čičak traka drži daljinske da ih ne gubiš.", "Serbian"),
                ("💡 Soda bikarbona rešava neprijatne mirise u torbi.", "Serbian"),
                ("💡 Sakrij novac iza futrole za telefon za hitne slučajeve.", "Serbian"),
                ("💡 Organizuj ostavu visećim držačem za cipele.", "Serbian"),
                ("💡 Podgrej picu u tiganju sa malo vode da korica ostane hrskava.", "Serbian"),
                ("💡 Stare majice iseci za krpe – štedi papir.", "Serbian")
            ]
            for text, lang in hacks:
                await db.execute("INSERT INTO hacks (text, language) VALUES (?, ?)", (text, lang))
        await db.commit()
        print("✅ Database initialized.")

async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_app():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

async def main():
    await init_db()
    await start_web_app()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
