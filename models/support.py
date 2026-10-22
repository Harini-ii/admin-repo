
import uuid

from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

from database import Base


class SupportTicket(Base):
    __tablename__ = "SUPPORT_TICKETS_HJ"
    __table_args__ = {"schema": "admin_hj"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    customer_id = Column(
        UUID(as_uuid=True),
        nullable=False,
    )

    customer_name = Column(
        String,
        nullable=True,
    )

    subject = Column(
        String,
        nullable=False,
    )

    message = Column(
        Text,
        nullable=False,
    )

    status = Column(
        String,
        nullable=False,
        default="OPEN",
    )

    reply = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
