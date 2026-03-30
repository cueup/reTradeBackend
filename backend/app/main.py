# FastAPI Entrypoint
from fastapi import FastAPI
from app.replay.ws import router as replay_router

app = FastAPI()

app.include_router(replay_router)