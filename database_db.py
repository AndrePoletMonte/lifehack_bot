import aiosqlite
from data.default_hacks import default_hacks

DB_NAME = "lifehack_bot.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                language TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS lifehacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                language TEXT,
                text TEXT
            )
        """)
        await db.execute("DELETE FROM lifehacks")

        for hack in default_hacks:
            await db.execute("INSERT INTO lifehacks (language, text) VALUES (?, ?)", (hack["language"], hack["text"]))
        await db.commit()
