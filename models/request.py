
# models/request.py

import uuid

from sqlalchemy import (
    Column,
    String,
    Integer,
    Numeric,
    Date,
    DateTime,
    Text,
    JSON,
    func,
)
from sqlalchemy.dialects.postgresql import UUID

from database import Base


class CustomerRequest(Base):
    __tablename__ = "CUSTOMER_REQUESTS_HJ"
    __table_args__ = {"schema": "admin_hj"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
    )
    request_number = Column(String, unique=True, nullable=False)
    request_type = Column(String, nullable=False)
    customer_id = Column(String, nullable=False)
    customer_name = Column(String, nullable=True)
    customer_email = Column(String, nullable=True)
    customer_mobile = Column(String, nullable=True)
    status = Column(String, nullable=False, default="Open")
    destination = Column(String, nullable=True)
    identity_document = Column(String, nullable=True)
    mode = Column(String, nullable=True)
    access = Column(String, nullable=True)
    service_type = Column(String(100), nullable=True)
    service_sub_type = Column(String(100), nullable=True)
    people_count = Column(Integer, nullable=True)
    budget = Column(Numeric(12, 2), nullable=True)
    currency = Column(String(10), nullable=True)
    department = Column(String(100), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    trip_type = Column(String(100), nullable=True)
    additional_requirements = Column(Text, nullable=True)
    customer_details = Column(JSON, nullable=True)
    service_details = Column(JSON, nullable=True)
    request_mode = Column(String(50), nullable=True)
    created_at = Column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class SalesRequest(Base):
    __tablename__ = "SALES_REQUESTS_HJ"
    __table_args__ = {"schema": "admin_hj"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
    )
    request_number = Column(String, unique=True, nullable=False)
    request_type = Column(String, nullable=False)
    customer_id = Column(String, nullable=False)
    customer_name = Column(String, nullable=True)
    customer_email = Column(String, nullable=True)
    customer_mobile = Column(String, nullable=True)
    status = Column(String, nullable=False, default="Open")
    destination = Column(String, nullable=True)
    identity_document = Column(String, nullable=True)
    mode = Column(String, nullable=True)
    access = Column(String, nullable=True)
    service_type = Column(String(100), nullable=True)
    service_sub_type = Column(String(100), nullable=True)
    people_count = Column(Integer, nullable=True)
    budget = Column(Numeric(12, 2), nullable=True)
    currency = Column(String(10), nullable=True)
    department = Column(String(100), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    trip_type = Column(String(100), nullable=True)
    additional_requirements = Column(Text, nullable=True)
    customer_details = Column(JSON, nullable=True)
    service_details = Column(JSON, nullable=True)
    request_mode = Column(String(50), nullable=True)
    created_at = Column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
