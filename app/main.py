
from app.db import MongoConnection
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.services.item_service import create_index_items
from app.services.vendor_service import create_index_vendor

from app.routers.item_router import router as item_router
from app.routers.vendor_router import router as vendor_router
from app.routers.item_vendor_router import router as item_vendor_router
from app.routers.purchase_order_router   import router as purchase_order_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    await MongoConnection.init()    
    
    await create_index_items()
    
    await create_index_vendor()
    
    yield  
    
    await MongoConnection.close()
    





app = FastAPI(
    title="Backend API Inventory Management",
    lifespan=lifespan
)


app.include_router(item_router)
app.include_router(vendor_router)
app.include_router(item_vendor_router)
app.include_router(purchase_order_router)