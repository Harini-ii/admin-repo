
import uuid

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

from database import Base


class SalesTeam(Base):
    __tablename__ ="SALES_TEAM_HJ" 
    __table_args__ = {"schema": "admin_hj"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    full_name = Column(String, nullable=False)

    email = Column(
        String,
        nullable=False,
        unique=True,
        index=True,
    )

    password_hash = Column(String, nullable=False)
    mobile_number = Column(String, nullable=False)
    department = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    identity_document = Column(String, nullable=True)

    joined_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    url = Column(String(500), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
