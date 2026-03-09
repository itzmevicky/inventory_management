from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime , timezone

from app.db import MongoWrapper

PO_COLLECTION = "purchase_orders"
REL_COLLECTION = "item_vendors"
ITEM_COLLECTION = "items"
VENDOR_COLLECTION = "vendors"

from app.schemas.purchase_order_schema import PurchaseOrderCreate

mongo = MongoWrapper()

async def create_purchase_order(data:PurchaseOrderCreate ):

    try:
        item_obj = ObjectId(data.item_id)
        vendor_obj = ObjectId(data.vendor_id)
    except Exception:
        raise HTTPException(400, "Invalid ObjectId")

    item = await mongo.find_one(ITEM_COLLECTION, {"_id": item_obj})
    if not item:
        raise HTTPException(404, "Item not found")

    vendor = await mongo.find_one(VENDOR_COLLECTION, {"_id": vendor_obj})
    if not vendor:
        raise HTTPException(404, "Vendor not found")

    relation = await mongo.find_one(
        REL_COLLECTION,
        {"item_id": item_obj, "vendor_id": vendor_obj}
    )

    if not relation:
        raise HTTPException(
            400,
            "Vendor is not approved to supply this item"
        )

    po_data = {
        "item_id": str(item_obj),
        "vendor_id": str(vendor_obj),
        "quantity": data.quantity,
        "status": "CREATED",
        "created_at": datetime.now(timezone.utc)
    }

    po_id = await mongo.insert_one(PO_COLLECTION, po_data)

    po_data["_id"] = po_id

    return po_data




async def get_purchase_orders():
    return await mongo.find_all(PO_COLLECTION)


async def get_purchase_order(po_id: str):

    try:
        obj_id = ObjectId(po_id)
    except Exception:
        raise HTTPException(400, "Invalid PO id")

    po = await mongo.find_one(PO_COLLECTION, {"_id": obj_id})

    if not po:
        raise HTTPException(404, "Purchase order not found")

    return po