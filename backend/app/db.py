import asyncpg
import os

# -------------------------
# DB CONNECTION
# -------------------------
pool = None

async def get_db():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(
            database="market_data_db",
            user="postgres",
            password="uLKjNalzwsmblGQ6",
            host="18.168.84.114",
            port=6543,
            min_size=5,
            max_size=20
    )

async def get_db_pool():
    return pool