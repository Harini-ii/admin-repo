import uuid

from sqlalchemy import Column, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from database import Base


class AircraftOperationalConfiguration(Base):
    __tablename__ = "AIRCRAFT_OPERATIONAL_CONFIGURATION_HJ"
    __table_args__ = {"schema": "admin_hj"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    aircraft_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    maximum_payload = Column(
        Numeric(12, 2),
        nullable=False
    )

    baggage_capacity = Column(
        Numeric(12, 2),
        nullable=False
    )

    configured_by = Column(
        UUID(as_uuid=True),
        nullable=True
    )
    config_at=Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

