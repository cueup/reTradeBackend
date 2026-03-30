# WebSocket Route (Replay Entry)
from fastapi import APIRouter, WebSocket
from app.replay.engine import start_replay

router = APIRouter()

@router.websocket("/ws/replay")
async def replay_ws(ws: WebSocket):
    await ws.accept()
    print("Client connected")

    try:
        await start_replay(ws)
    except Exception as e:
        print("WebSocket error:", e)
    finally:
        print("Client disconnected")