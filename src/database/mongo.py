from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.config import settings


MONGODB_URL = (
    "mongodb://"
    f"{settings.mongo_username}:{settings.mongo_password}"
    f"@{settings.mongo_hostname}"
    "?retryWrites=true&w=majority"
)
mongo_client = AsyncIOMotorClient(MONGODB_URL)
mongo_db = mongo_client.get_database(settings.mongo_db_name)


async def get_or_create_collection(db: AsyncIOMotorDatabase, collection_name: str):
    collections = await db.list_collection_names()
    if collection_name not in collections:
        collection = db.create_collection(collection_name)
    else:
        collection = db.get_collection(collection_name)
    return collection


async def get_mongo_db():
    global mongo_client, mongo_db
    mongo_session = await mongo_client.start_session()
    try:
        yield mongo_db
    finally:
        await mongo_session.end_session()
