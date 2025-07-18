import aiosqlite

async def create_tables():
    async with aiosqlite.connect("lifehack_bot.db") as db:
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
            content TEXT
        )
        """)
        await db.commit()
