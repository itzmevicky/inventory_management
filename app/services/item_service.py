from bson import ObjectId
from app.db import MongoWrapper 
from fastapi import HTTPException
from app.models.item_model import item_helper


mongo = MongoWrapper()


COLLECTION_NAME = "items"

async def create_item(data: dict):

    existing = await mongo.find_one(
        COLLECTION_NAME,
        {"sku": data["sku"]}
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="SKU already exists"
        )

    item_id = await mongo.insert_one(
        COLLECTION_NAME,
        data
    )

    data["_id"] = item_id

    return item_helper(data)

async def get_items():

    items = await mongo.find_all(
        COLLECTION_NAME
    )
    
    return [item_helper(i) for i in items]

async def get_item(item_id: str):

    try:
        obj_id = ObjectId(item_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid item_id format"
        )

    item = await mongo.find_one(
        COLLECTION_NAME,
        {"_id": obj_id}
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return item_helper(item)

async def update_item(item_id: str, data: dict):

    try:
        obj_id = ObjectId(item_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid item_id format"
        )

    updated = await mongo.update_one(
        COLLECTION_NAME,
        {"_id": obj_id},
        data
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    item = await mongo.find_one(
        COLLECTION_NAME,
        {"_id": obj_id}
    )

    return item

async def delete_item(item_id: str):

    try:
        obj_id = ObjectId(item_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid item_id format"
        )

    deleted = await mongo.delete_one(
        COLLECTION_NAME,
        {"_id": obj_id}
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return {"message": "Item deleted successfully"}

async def create_index_items():
    await mongo.create_index(
            "items",
            [("sku", 1)],
            unique=True
        )