from fastapi import APIRouter, WebSocket
from app.live.engine import live_stream

router = APIRouter()

@router.websocket("/ws/live")
async def live_ws(ws: WebSocket):
    await ws.accept()
    print("Client connected")

    while True:
        msg = await ws.receive_json()

        if msg["action"] == "subscribe":
            symbol = msg["symbol"]

            print(f"Subscribing to {symbol}")
        await live_stream(ws, symbol)