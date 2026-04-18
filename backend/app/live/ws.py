from fastapi import APIRouter, WebSocket
from app.live.engine import live_stream

router = APIRouter()

@router.websocket("/ws/live")
async def live_ws(ws: WebSocket):
    await ws.accept()
    print("Client connected")

    try:
        await live_stream(ws)
    except Exception as e:
        print("WebSocket error:", e)
    finally:
        print("Client disconnected")

    symbol = "EURUSD"  # later from client
    await live_stream(ws, symbol)