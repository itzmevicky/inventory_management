from bson import ObjectId
from fastapi import HTTPException
from app.db import MongoWrapper 
from app.models.vendor_model import  vendor_helper

COLLECTION_NAME = "vendors"


mongo = MongoWrapper()


async def create_vendor(data: dict):

    existing = await mongo.find_one(
        COLLECTION_NAME,
        {"email": data["email"]}
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Vendor with this email already exists"
        )

    vendor_id = await mongo.insert_one(
        COLLECTION_NAME,
        data
    )

    data['_id'] = vendor_id
    
    return vendor_helper(data)


async def get_vendors():

    vendors = await mongo.find_all(COLLECTION_NAME)

    return [vendor_helper(v) for v in vendors]


async def get_vendor(vendor_id: str):

    try:
        obj_id = ObjectId(vendor_id)
    except Exception:
        raise HTTPException(400, "Invalid vendor_id format")

    vendor = await mongo.find_one(
        COLLECTION_NAME,
        {"_id": obj_id}
    )

    if not vendor:
        raise HTTPException(404, "Vendor not found")

    return vendor_helper(vendor)


async def update_vendor(vendor_id: str, data: dict):

    try:
        obj_id = ObjectId(vendor_id)
    except Exception:
        raise HTTPException(400, "Invalid vendor_id format")

    if not data:
        raise HTTPException(400, "No fields provided for update")

    updated = await mongo.update_one(
        COLLECTION_NAME,
        {"_id": obj_id},
        data
    )

    if not updated:
        raise HTTPException(404, "Vendor not found")

    vendor = await mongo.find_one(
        COLLECTION_NAME,
        {"_id": obj_id}
    )

    return vendor_helper(vendor)


async def delete_vendor(vendor_id: str):

    try:
        obj_id = ObjectId(vendor_id)
    except Exception:
        raise HTTPException(400, "Invalid vendor_id format")

    deleted = await mongo.delete_one(
        COLLECTION_NAME,
        {"_id": obj_id}
    )

    if not deleted:
        raise HTTPException(404, "Vendor not found")

    return {"message": "Vendor deleted successfully"}




async def create_index_vendor():
    await mongo.create_index(
            "vendors",
            [("email", 1)],
            unique=True
        )
    
    await mongo.create_index(
            "vendors",
            [("name", 1)]
        )
    
    
    await mongo.create_index(
            "item_vendors",
            [("item_id", 1), ("vendor_id", 1)],
            unique=True
        )