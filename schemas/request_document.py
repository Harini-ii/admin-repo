
# schemas/request_document.py

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RequestDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    request_id: UUID
    customer_id: UUID
    storage_path: str
    original_filename: str
    mime_type: str | None = None
    file_size: int
    document_type: str | None = None
    created_at: datetime


class CustomerRequestDocumentResponse(RequestDocumentResponse):
    pass


class SalesRequestDocumentResponse(RequestDocumentResponse):
    pass
