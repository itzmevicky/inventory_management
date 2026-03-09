# # Your MongoWrapper
from motor.motor_asyncio import AsyncIOMotorClient
from collections.abc import Mapping

import pymongo

from app.logger import get_logger
from app.constants import MONGO_URI, DATABASE_NAME

logger = get_logger("MONGO")


class MongoConnection:
    _client = None
    _db = None

    @classmethod
    async def init(cls):
        if cls._client is not None:
            return cls._db

        if not MONGO_URI.startswith(("mongodb://", "mongodb+srv://")):
            raise ValueError(f"Invalid MongoDB URI: {MONGO_URI}")

        try:
            cls._client = AsyncIOMotorClient(MONGO_URI)
            cls._db = cls._client[DATABASE_NAME]
            logger.info("MongoDB connected successfully", db_name=DATABASE_NAME)
        except pymongo.errors.InvalidURI as e:
            logger.error("MongoDB Connection Error", error=str(e), uri=MONGO_URI)
            raise
        except Exception as e:
            logger.exception("Unexpected error during MongoDB init")
            raise

        return cls._db


    @classmethod
    def get_db(cls):
        if cls._db is None:
            raise RuntimeError("MongoDB not initialized. Call init() first.")
        return cls._db
    
    
    @classmethod
    async def close(cls):
        if cls._client is not None:
            cls._client.close()
            cls._client = None
            cls._db = None
            logger.info("MongoDB connection closed")
            

class MongoWrapper:
    def __init__(self):
        self._db = None

    def _ensure_db(self):
        if self._db is None:
            self._db = MongoConnection.get_db()
        if self._db is None:
            raise RuntimeError("MongoDB not initialized. Call init() first.")

    async def insert_one(self, collection_name: str, data: Mapping) -> str:
        self._ensure_db()
        result = await self._db[collection_name].insert_one(data)
        return str(result.inserted_id)

    async def insert_many(self, collection_name: str, documents: list[dict]):
        self._ensure_db()
        if not documents:
            return {"inserted_count": 0}

        result = await self._db[collection_name].insert_many(documents , ordered=False)
        return {"inserted_count": len(result.inserted_ids)}
    
    async def find_one(self, collection_name: str, filter: Mapping, **kwargs) -> dict | None:
        self._ensure_db()
        doc = await self._db[collection_name].find_one(filter, **kwargs)
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def find_all(self, collection_name: str, filter: Mapping = {}, **kwargs) -> list[dict]:
        self._ensure_db()   
        cursor = self._db[collection_name].find(filter, **kwargs)
        docs = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            docs.append(doc)
        return docs

    async def update_one(self, collection_name: str, filter: Mapping, update_data: Mapping, **kwargs) -> bool:
        self._ensure_db()
        result = await self._db[collection_name].update_one(filter, {"$set": update_data}, **kwargs)
        return result.modified_count > 0

    async def delete_one(self, collection_name: str, filter: Mapping, **kwargs) -> bool:
        self._ensure_db()
        result = await self._db[collection_name].delete_one(filter, **kwargs)
        return result.deleted_count > 0
    
    async def create_index(self, collection_name: str, index_fields: list, **kwargs):
        self._ensure_db()
        return await self._db[collection_name].create_index(index_fields,**kwargs)