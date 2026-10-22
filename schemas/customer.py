from pydantic import BaseModel, EmailStr


class CustomerResponse(BaseModel):
    id: str
    name: str | None = None
    email: EmailStr
    mobile: str | None = None
    country: str | None = None
    company: str | None = None
    joined_at: object

    class Config:
        from_attributes = True