from fastapi import APIRouter
from app.schemas.vendor_schema import VendorCreate, VendorUpdate
from app.services.vendor_service import (
    create_vendor,
    get_vendors,
    get_vendor,
    update_vendor,
    delete_vendor
)

router = APIRouter(prefix="/vendors", tags=["Vendors"])


@router.post("/")
async def create_vendor_api(vendor: VendorCreate):
    return await create_vendor(vendor.model_dump())


@router.get("/")
async def get_vendors_api():
    return await get_vendors()


@router.get("/{vendor_id}")
async def get_vendor_api(vendor_id: str):
    return await get_vendor(vendor_id)


@router.patch("/{vendor_id}")
async def update_vendor_api(vendor_id: str, vendor: VendorUpdate):
    return await update_vendor(vendor_id, vendor.model_dump(exclude_none=True))


@router.delete("/{vendor_id}")
async def delete_vendor_api(vendor_id: str):
    return await delete_vendor(vendor_id)