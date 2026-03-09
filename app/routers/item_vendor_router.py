from fastapi import APIRouter

from app.services.item_vendor_service import (
    link_vendor_to_item,
    get_vendors_for_item,
    get_items_for_vendor,
    unlink_vendor_from_item
)

router = APIRouter(tags=["Item Vendor Relations"])


@router.post("/items/{item_id}/vendors/{vendor_id}")
async def link_vendor(item_id: str, vendor_id: str):
    return await link_vendor_to_item(item_id, vendor_id)


@router.get("/items/{item_id}/vendors")
async def get_item_vendors(item_id: str):
    return await get_vendors_for_item(item_id)


@router.get("/vendors/{vendor_id}/items")
async def get_vendor_items(vendor_id: str):
    return await get_items_for_vendor(vendor_id)


@router.delete("/items/{item_id}/vendors/{vendor_id}")
async def unlink_vendor(item_id: str, vendor_id: str):
    return await unlink_vendor_from_item(item_id, vendor_id)