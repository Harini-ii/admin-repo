
# schemas/request.py

from datetime import date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RequestFields(BaseModel):
    request_number: str
    request_type: str
    customer_id: str

    customer_name: str | None = None
    customer_email: str | None = None
    customer_mobile: str | None = None
    status: str = "Open"
    destination: str | None = None
    identity_document: str | None = None
    mode: str | None = None
    access: str | None = None
    service_type: str | None = None
    service_sub_type: str | None = None
    people_count: int | None = None
    budget: Decimal | None = None
    currency: str | None = None
    department: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    trip_type: str | None = None
    additional_requirements: str | None = None
    customer_details: dict[str, Any] | list[Any] | None = None
    service_details: dict[str, Any] | list[Any] | None = None
    request_mode: str | None = None


class CustomerRequestCreate(RequestFields):
    pass


class SalesRequestCreate(RequestFields):
    pass


class CustomerRequestUpdate(BaseModel):
    request_number: str | None = None
    request_type: str | None = None
    customer_id: str | None = None
    customer_name: str | None = None
    customer_email: str | None = None
    customer_mobile: str | None = None
    status: str | None = None
    destination: str | None = None
    identity_document: str | None = None
    mode: str | None = None
    access: str | None = None
    service_type: str | None = None
    service_sub_type: str | None = None
    people_count: int | None = None
    budget: Decimal | None = None
    currency: str | None = None
    department: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    trip_type: str | None = None
    additional_requirements: str | None = None
    customer_details: dict[str, Any] | list[Any] | None = None
    service_details: dict[str, Any] | list[Any] | None = None
    request_mode: str | None = None


class SalesRequestUpdate(CustomerRequestUpdate):
    pass


class CustomerRequestResponse(RequestFields):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime


class SalesRequestResponse(CustomerRequestResponse):
    pass
