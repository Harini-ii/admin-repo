
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

    name = Column(String(150), nullable=True)
    email = Column(String(255), nullable=True)
    phone_number = Column(String(30), nullable=True)

    # Sensitive field: never return this in an API response.
    password = Column(String(255), nullable=True)

    role = Column(String(100), nullable=True)
    company = Column(String(150), nullable=True)
    country = Column(String(100), nullable=True)
    profile_url = Column(String(500), nullable=True)

    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
