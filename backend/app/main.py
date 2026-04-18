# FastAPI Entrypoint
from fastapi import FastAPI
from app.replay.ws import router as replay_router
from app.live.ws import router as live_router
from app.db import get_db

app = FastAPI()

@app.lifespan("startup")
async def startup():
    await get_db()
    print("Database connection pool created")

app.include_router(replay_router)
app.include_router(live_router)

@app.get("/")
def root():
    return {"status": "running"}