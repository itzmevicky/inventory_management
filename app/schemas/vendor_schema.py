from pydantic import BaseModel, Field, EmailStr

class VendorCreate(BaseModel):
    name: str = Field(..., example="FreshFarm")
    email: EmailStr = Field(..., example="contact@freshfarm.com")
    phone: str | None = Field(None, example="9999999999")

class VendorUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None

