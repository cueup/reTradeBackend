import asyncio
from app.db import get_db_pool

async def live_stream(ws, symbol):

    pool = await get_db_pool()
    last_ts = None

    while True:

        query = """
        SELECT timestamp, open, high, low, close
        FROM candles
        WHERE symbol=$1
        ORDER BY timestamp DESC
        LIMIT 1
        """

        async with pool.acquire() as conn:
            row = await conn.fetchrow(query, symbol)

        if row and row["timestamp"] != last_ts:

            last_ts = row["timestamp"]

            await ws.send_json({
                "t": row["timestamp"].isoformat(),
                "o": float(row["open"]),
                "h": float(row["high"]),
                "l": float(row["low"]),
                "c": float(row["close"])
            })

        await asyncio.sleep(1)