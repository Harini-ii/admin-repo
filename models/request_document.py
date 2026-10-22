
# models/request_document.py

import uuid

from sqlalchemy import Column, String, DateTime, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from database import Base


class CustomerRequestDocument(Base):
    __tablename__ = "CUSTOMER_REQUEST_DOCUMENTS_HJ"
    __table_args__ = {"schema": "admin_hj"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    request_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    customer_id = Column(UUID(as_uuid=True), nullable=False)
    storage_path = Column(String, nullable=False)
    original_filename = Column(String(255), nullable=False)
    mime_type = Column(String(150), nullable=True)
    file_size = Column(BigInteger, nullable=False)
    document_type = Column(String(100), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class SalesRequestDocument(Base):
    __tablename__ = "SALES_REQUEST_DOCUMENTS_HJ"
    __table_args__ = {"schema": "admin_hj"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    request_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    customer_id = Column(UUID(as_uuid=True), nullable=False)
    storage_path = Column(String, nullable=False)
    original_filename = Column(String(255), nullable=False)
    mime_type = Column(String(150), nullable=True)
    file_size = Column(BigInteger, nullable=False)
    document_type = Column(String(100), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
