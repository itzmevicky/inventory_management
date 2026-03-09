from pydantic import BaseModel, Field

class PurchaseOrderCreate(BaseModel):
    item_id: str
    vendor_id: str
    quantity: int = Field(gt=0)


