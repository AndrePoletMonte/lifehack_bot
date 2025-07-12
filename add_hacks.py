import aiosqlite
import asyncio
import os

DB_PATH = "lifehack_bot.db"

async def create_tables_and_add_hacks():
    hacks = [
        "Use a binder clip to organize cables on your desk.",
        "Put a wooden spoon across a boiling pot to prevent it from boiling over.",
        "Use a clothespin to hold a nail when hammering to protect your fingers."
    ]

    # Создание базы и таблицы
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS hacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                language TEXT DEFAULT 'English',
                used INTEGER DEFAULT 0
            )
        """)
        await db.commit()

        # Добавление лайфхаков
        for hack in hacks:
            await db.execute(
                "INSERT INTO hacks (text, language, used) VALUES (?, ?, ?)",
                (hack, 'English', 0)
            )
        await db.commit()
        print("✅ Hacks added successfully.")

asyncio.run(create_tables_and_add_hacks())
