import asyncio
import aiosqlite

async def add_test_hacks():
    async with aiosqlite.connect("lifehack_bot.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS hacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                language TEXT,
                used INTEGER DEFAULT 0
            )
        """)
        # 
        await db.executemany("""
            INSERT INTO hacks (text, language, used) VALUES (?, ?, 0)
        """, [
            ("Drink a glass of water right after you wake up.", "English"),
            ("Take 5 deep breaths whenever you feel stressed.", "English"),
            ("Write down 3 things you are grateful for each day.", "English")
        ])
        await db.commit()
    print("Test lifehacks added to database.")

if __name__ == "__main__":
    asyncio.run(add_test_hacks())
