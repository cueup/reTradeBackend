import asyncpg
import os

# -------------------------
# DB CONNECTION
# -------------------------

async def get_db():
    return await asyncpg.create_pool(
        database="market_data_db",
        user="postgres",
        password="uLKjNalzwsmblGQ6",
        host="srv-captain--timescaledb",
        port=6543
    )