
import uuid

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from database import Base


class Customer(Base):
    __tablename__ = "CUSTOMER_PROFILE"
    __table_args__ = {"schema": "customer_hj"}

    customer_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    name = Column(String(150))
    email = Column(String(255))
    phone_number = Column(String(30))
    password = Column(String(255))
    created_at = Column(DateTime)
    country = Column(String(100), nullable=True)
    company = Column(String(150), nullable=True)
