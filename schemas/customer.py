
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: UUID
    name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    role: str | None = None
    company: str | None = None
    country: str | None = None
    profile_url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
