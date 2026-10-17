from motor.motor_asyncio import AsyncIOMotorClient
from core.config import MONGODB_URI, MONGODB_DATABASE

client = AsyncIOMotorClient(MONGODB_URI)

database = client[MONGODB_DATABASE]

productos_collection = database["catalogo"]