from fastapi import APIRouter
from app.schemas.item_schema import ItemCreate, ItemUpdate


from app.services.item_service import (
    create_item,
    get_items,
    get_item,
    update_item,
    delete_item
)

from app.services.item_vendor_service import link_vendor_to_item




router = APIRouter(prefix="/items", tags=["Items"])



@router.post("/")
async def create_item_api(item: ItemCreate):
    return await create_item(item.model_dump())



@router.get("/")
async def get_items_api():

    return await get_items()

@router.get("/{item_id}")
async def get_item_api(item_id: str):

    return await get_item(item_id)


@router.patch("/{item_id}")
async def update_item_api(item_id: str, item: ItemUpdate):

    return await update_item(item_id, item.dict(exclude_none=True))



@router.delete("/{item_id}")
async def delete_item_api(item_id: str):

    return await delete_item(item_id)




