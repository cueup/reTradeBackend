# Replay Engine (Core Logic)
import asyncio
from datetime import datetime
from app.db import get_db

class ReplaySession:
    def __init__(self, symbol, timeframe, start_time):
        self.symbol = symbol
        self.timeframe = timeframe
        self.current_time = start_time
        self.speed = 1
        self.playing = False


async def fetch_candles(pool, symbol, start):

    query = """
        SELECT timestamp, open, high, low, close
        FROM candles
        WHERE symbol=$1 AND timestamp >= $2
        ORDER BY timestamp
        LIMIT 500
    """
    async with pool.acquire() as conn:
        rows = await conn.fetch(query, symbol, start)
    print(f"Fetched {len(rows)} candles")
    return rows


async def start_replay(ws):

    pool = await get_db()
    session = None
    buffer = []

    while True:

        msg = await ws.receive_json()

        if msg["action"] == "start":

            session = ReplaySession(
                msg["symbol"],
                msg["timeframe"],
                datetime.fromisoformat(msg["start_time"])
            )

            session.playing = True

            asyncio.create_task(run_loop(ws, session, pool, buffer))

        elif msg["action"] == "play":
            session.playing = True

        elif msg["action"] == "pause":
            session.playing = False

        elif msg["action"] == "speed":
            session.speed = msg["value"]


async def run_loop(ws, session, pool, buffer):

    try:
        while True:

            if not session.playing:
                await asyncio.sleep(0.1)
                continue

            if len(buffer) < 50:
                rows = await fetch_candles(pool, session.symbol, session.current_time)
                buffer.extend(rows)

            if not buffer:
                await ws.send_json({"type": "end"})
                break

            candle = buffer.pop(0)
            session.current_time = candle["timestamp"]

            await ws.send_json({
                "t": candle["timestamp"].isoformat(),
                "o": float(candle["open"]),
                "h": float(candle["high"]),
                "l": float(candle["low"]),
                "c": float(candle["close"])
            })

            await asyncio.sleep(1 / session.speed)

    except Exception as e:
        print("Replay loop crashed:", e)
        await ws.close()