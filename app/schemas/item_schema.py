from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(..., example="Apple")
    sku: str = Field(..., example="APL001")
    stock: int = Field(..., example=100)


class ItemUpdate(BaseModel):
    name: str | None = None
    sku: str | None = None
    stock: int | None = None



    