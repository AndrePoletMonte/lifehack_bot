

import aiosqlit
async def create_lifehacks_table():
    async with aiosqlite.connect("lifehack_bot.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS lifehacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text_en TEXT NOT NULL,
                text_sr TEXT NOT NULL
            )
        """)
        await db.commit
async def add_lifehack(text_en: str, text_sr: str):
    async with aiosqlite.connect("lifehack_bot.db") as db:
        await db.execute(
            "INSERT INTO lifehacks (text_en, text_sr) VALUES (?, ?)",
            (text_en, text_sr)
        )
        await db.commit()

async def get_random_lifehack():
    async with aiosqlite.connect("lifehack_bot.db") as db:
        async with db.execute("SELECT text_en, text_sr FROM lifehacks ORDER BY RANDOM() LIMIT 1") as cursor:
            row = await cursor.fetchone()
            return row if row else None

async def get_all_lifehacks():
    async with aiosqlite.connect("lifehack_bot.db") as db:
        async with db.execute("SELECT text_en, text_sr FROM lifehacks") as cursor:
            return await cursor.fetchall()
