import uuid

from sqlalchemy import Column, DateTime, String, Float, ForeignKey,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from database import Base


class Aircraft(Base):
    __tablename__ ="AIRCRAFT_HJ"
    __table_args__ = {"schema": "admin_hj"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    model = Column(String, nullable=False)
    type = Column(String, nullable=False)
    seating = Column(Integer, nullable=False)
    image = Column(String, nullable=True)
    maximum_payload = Column(Float, nullable=True)
    baggage_capacity = Column(Float, nullable=True)


class AircraftImage(Base):
    __tablename__ = "AIRCRAFT_IMAGES_HJ"
    __table_args__ = {"schema": "admin_hj"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    aircraft_id = Column(
        UUID(as_uuid=True),
        ForeignKey("admin_hj.AIRCRFT_HJ.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    model = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)
    seats = Column(Integer, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    image_url = Column(String(1000), nullable=False)