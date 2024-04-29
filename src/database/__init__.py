from contextlib import asynccontextmanager
from fastapi import FastAPI
from icecream import ic

from .mongo import mongo_client
from .postgres import engine
from src.message_queue import queue


@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine, mongo_client

    # on startup
    ic("Database connections successfully established!")
    yield

    # on shutdown
    engine.dispose()
    mongo_client.close()
    await queue.aclose()
    ic("Database connections successfully closed!")
