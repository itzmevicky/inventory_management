from fastapi import APIRouter
from app.schemas.purchase_order_schema import PurchaseOrderCreate

from app.services.purchase_order_service import (
    create_purchase_order,
    get_purchase_orders,
    get_purchase_order
)

router = APIRouter(prefix="/purchase-orders", tags=["Purchase Orders"])




@router.post("/")
async def create_po(po: PurchaseOrderCreate):

    return await create_purchase_order(
       data=po
    )

@router.get("/")
async def list_po():
    return await get_purchase_orders()


@router.get("/{po_id}")
async def get_po(po_id: str):
    return await get_purchase_order(po_id)