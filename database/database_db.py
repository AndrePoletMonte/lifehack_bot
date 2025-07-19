import aiosqlite

DB_PATH = "lifehack_bot.db"

async def add_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.commit()

async def set_language(user_id: int, language: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET language = ? WHERE user_id = ?", (language, user_id))
        await db.commit()

async def get_random_lifehack(language: str) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT text FROM lifehacks WHERE language = ? ORDER BY RANDOM() LIMIT 1", (language,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else "No lifehacks available yet."
