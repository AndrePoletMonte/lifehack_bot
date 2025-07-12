import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from datetime import datetime
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
import aiosqlite
from aiogram.client.default import DefaultBotProperties

API_TOKEN = "8051188469:AAGAv6h_jZ_d4TzKiOI3DgwoGiPCus4err4"

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()
router = Router()
dp.include_router(router)

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Get Lifehack")],
            [KeyboardButton(text="🔁 Reset Lifehacks")],
            [KeyboardButton(text="🌍 Change Language")],
            [KeyboardButton(text="📂 Change Categories")]
        ],
        resize_keyboard=True
    )
@router.message(F.text == "🌍 Change Language")
@router.message(F.text.in_(["English", "Serbian"]))
async def save_language(message: Message):
    user_language = message.text

    async with aiosqlite.connect("lifehack_bot.db") as db:
        await db.execute(
            "UPDATE users SET language = ? WHERE telegram_id = ?",
            (user_language, message.from_user.id)
        )
        await db.commit()

    await message.answer(
        f"✅ Language set to {user_language}.",
        reply_markup=get_main_keyboard()
    )

async def change_language(message: Message):
    language_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="English"), KeyboardButton(text="Serbian")],
            [KeyboardButton(text="⬅️ Back")]
        ],
        resize_keyboard=True
    )

    await message.answer("Choose your language:", reply_markup=language_keyboard)


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
                ("💡 Use a binder clip to organize charging cables on your desk.", "English"),
                ("💡 Put a wooden spoon across a boiling pot to stop it from boiling over.", "English"),
                ("💡 Take a photo of your fridge before shopping to remember what you need.", "English"),
                ("💡 Use airplane mode while charging to speed it up.", "English"),
                ("💡 Use Ctrl+Shift+T to reopen the last closed browser tab.", "English"),
                ("💡 Store natural peanut butter upside down to prevent oil separation.", "English"),
                ("💡 Користи спајалицу да организујеш каблове за пуњење на столу.", "Serbian"),
                ("💡 Стави дрвену кашику преко лонца да не покипи.", "Serbian"),
                ("💡 Сликај фрижидер пре одласка у продавницу.", "Serbian"),
                ("💡 Укључи airplane mode да брже напуниш батерију.", "Serbian")
            ]
            for text, lang in hacks:
                await db.execute("INSERT INTO hacks (text, language) VALUES (?, ?)", (text, lang))

        await db.commit()

@router.message(Command("start"))
async def cmd_start(message: Message):
    async with aiosqlite.connect("lifehack_bot.db") as db:
        await db.execute("""
            INSERT OR IGNORE INTO users (telegram_id, language, categories, joined_at)
            VALUES (?, ?, ?, ?)
        """, (
            message.from_user.id,
            message.from_user.language_code or 'English',
            'Productivity,Health,Mindfulness',
            datetime.now()
        ))
        await db.commit()

    await message.answer(
        "✅ Welcome to LifehackDrop!\nYou'll receive daily lifehacks to improve your day.\nPress the button below to get one:",
        reply_markup=get_main_keyboard()
    )

@router.message(F.text == "Get Lifehack")
async def get_lifehack(message: Message):
    async with aiosqlite.connect("lifehack_bot.db") as db:
        cursor = await db.execute(
            "SELECT language FROM users WHERE telegram_id = ?",
            (message.from_user.id,)
        )
        row = await cursor.fetchone()
        user_language = row[0] if row else "English"

        async with db.execute("""
            SELECT id, text FROM hacks
            WHERE used = 0 AND language = ?
            ORDER BY RANDOM() LIMIT 1
        """, (user_language,)) as cursor:
            row = await cursor.fetchone()

        if row:
            hack_id, hack_text = row
            await message.answer(hack_text)
            await db.execute("UPDATE hacks SET used = 1 WHERE id = ?", (hack_id,))
            await db.execute("""
                INSERT INTO stats (user_id, hack_id, sent_at)
                VALUES (?, ?, ?)
            """, (message.from_user.id, hack_id, datetime.now()))
            await db.commit()
        else:
            await message.answer("No more lifehacks available. Stay tuned!")

@router.message(F.text == "🔁 Reset Lifehacks")
async def reset_lifehacks(message: Message):
    async with aiosqlite.connect("lifehack_bot.db") as db:
        await db.execute("UPDATE hacks SET used = 0")
        await db.commit()
    await message.answer("🔄 Lifehacks have been reset. You can receive them again.")

@router.message(F.text == "🌍 Change Language")
async def change_language(message: Message):
    await message.answer(
        "🌐 Choose language:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="English"), KeyboardButton(text="Serbian")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )
@router.message(F.text.in_(["🇺🇸 English", "🇷🇸 Serbian"]))
async def change_language(message: Message):
    new_lang = "English" if message.text == "🇺🇸 English" else "Serbian"

    async with aiosqlite.connect("lifehack_bot.db") as db:
        await db.execute("""
            UPDATE users SET language = ? WHERE telegram_id = ?
        """, (new_lang, message.from_user.id))
        await db.commit()

   @router.message(F.text.in_(["English", "Serbian"]))
async def save_language(message: Message):
    new_lang = message.text

    async with aiosqlite.connect("lifehack_bot.db") as db:
        await db.execute(
            "UPDATE users SET language = ? WHERE telegram_id = ?",
            (new_lang, message.from_user.id)
        )
        await db.commit()

    await message.answer(
        f"✅ Language set to {new_lang}.",
        reply_markup=get_main_keyboard()
    )

   
@router.message(F.text == "📂 Change Categories")
async def change_categories(message: Message):
    await message.answer(
        "📌 Select your favorite categories (send as comma-separated list):\nExample: Productivity,Health,Mindfulness\n\nAvailable: Productivity, Health, Mindfulness, Tech, Money",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Cancel")]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

if __name__ == "__main__":
    asyncio.run(main())
