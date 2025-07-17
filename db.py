import os
import asyncpg
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def connect():
    return await asyncpg.connect(DATABASE_URL)

async def add_user_if_not_exists(user_id):
    conn = await connect()
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            user_id BIGINT UNIQUE
        )
    """)
    await conn.execute("""
        INSERT INTO users (user_id) 
        VALUES ($1) 
        ON CONFLICT (user_id) DO NOTHING
    """, user_id)
    await conn.close()

async def get_random_lifehack():
    conn = await connect()
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS lifehacks (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL
        )
    """)
    row = await conn.fetchrow("SELECT text FROM lifehacks ORDER BY RANDOM() LIMIT 1")
    await conn.close()
    return row['text'] if row else "😔 No lifehacks found. Add some first."
