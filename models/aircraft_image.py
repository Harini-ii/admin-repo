import uuid

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from database import Base


class AircraftImage(Base):
    __tablename__ = "AIRCRAFT_IMAGES_HJ"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    model = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    seats = Column(Integer, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    image_url = Column(String(1000), nullable=False)