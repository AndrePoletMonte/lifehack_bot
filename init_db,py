import asyncio
from db import connect

async def init_db():
    conn = await connect()
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            user_id BIGINT UNIQUE
        )
    """)
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS lifehacks (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL
        )
    """)
    await conn.close()
    print("✅ Tables created successfully.")

if __name__ == "__main__":
    asyncio.run(init_db())
