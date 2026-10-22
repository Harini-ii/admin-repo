
# models/request_timeline.py

import uuid

from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from database import Base


class CustomerRequestTimeline(Base):
    __tablename__ = "CUSTOMER_REQUEST_TIMELINE_HJ"
    __table_args__ = {"schema": "admin_hj"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    request_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    actor_id = Column(UUID(as_uuid=True), nullable=True)
    event_type = Column(String(100), nullable=False)
    messages = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    actor_role = Column(String(100), nullable=True)
    passenger_id = Column(UUID(as_uuid=True), nullable=True)
    passenger_document_id = Column(UUID(as_uuid=True), nullable=True)


class SalesRequestTimeline(Base):
    __tablename__ = "SALES_REQUEST_TIMELINE_HJ"
    __table_args__ = {"schema": "admin_hj"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    request_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    actor_id = Column(UUID(as_uuid=True), nullable=True)
    event_type = Column(String(100), nullable=False)
    messages = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    actor_role = Column(String(100), nullable=True)
    passenger_id = Column(UUID(as_uuid=True), nullable=True)
    passenger_document_id = Column(UUID(as_uuid=True), nullable=True)
