from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime

from app.db import MongoWrapper 

REL_COLLECTION = "item_vendors"
ITEM_COLLECTION = "items"
VENDOR_COLLECTION = "vendors"



mongo = MongoWrapper()

async def link_vendor_to_item(item_id: str, vendor_id: str):

    try:
        item_obj = ObjectId(item_id)
        vendor_obj = ObjectId(vendor_id)
    except Exception:
        raise HTTPException(400, "Invalid ObjectId")

    item = await mongo.find_one(ITEM_COLLECTION, {"_id": item_obj})
    if not item:
        raise HTTPException(404, "Item not found")

    vendor = await mongo.find_one(VENDOR_COLLECTION, {"_id": vendor_obj})
    if not vendor:
        raise HTTPException(404, "Vendor not found")

    existing = await mongo.find_one(
        REL_COLLECTION,
        {"item_id": item_obj, "vendor_id": vendor_obj}
    )

    if existing:
        raise HTTPException(409, "Vendor already linked to item")

    data = {
        "item_id": item_obj,
        "vendor_id": vendor_obj,
        "created_at": datetime.utcnow()
    }

    await mongo.insert_one(REL_COLLECTION, data)

    return {"message": "Vendor linked to item"}


async def get_vendors_for_item(item_id: str):

    try:
        item_obj = ObjectId(item_id)
    except Exception:
        raise HTTPException(400, "Invalid item_id")

    relations = await mongo.find_all(
        REL_COLLECTION,
        {"item_id": item_obj}
    )

    vendor_ids = [ObjectId(rel["vendor_id"]) for rel in relations]

    if not vendor_ids:
        return []

    vendors = await mongo.find_all(
        VENDOR_COLLECTION,
        {"_id": {"$in": vendor_ids}}
    )

    return vendors


async def get_items_for_vendor(vendor_id: str):

    try:
        vendor_obj = ObjectId(vendor_id)
    except Exception:
        raise HTTPException(400, "Invalid vendor_id")

    relations = await mongo.find_all(
        REL_COLLECTION,
        {"vendor_id": vendor_obj}
    )

    item_ids = [ObjectId(rel["item_id"]) for rel in relations]

    if not item_ids:
        return []

    items = await mongo.find_all(
        ITEM_COLLECTION,
        {"_id": {"$in": item_ids}}
    )

    return items


async def unlink_vendor_from_item(item_id: str, vendor_id: str):

    try:
        item_obj = ObjectId(item_id)
        vendor_obj = ObjectId(vendor_id)
    except Exception:
        raise HTTPException(400, "Invalid ObjectId")

    deleted = await mongo.delete_one(
        REL_COLLECTION,
        {"item_id": item_obj, "vendor_id": vendor_obj}
    )

    if not deleted:
        raise HTTPException(404, "Relationship not found")

    return {"message": "Vendor removed from item"}