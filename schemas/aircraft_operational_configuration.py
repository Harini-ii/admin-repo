from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AircraftOperationalConfigurationCreate(BaseModel):
    aircraft_id: UUID
    maximum_payload: Decimal = Field(gt=0)
    baggage_capacity: Decimal = Field(ge=0)
    configured_by: UUID | None = None


class AircraftOperationalConfigurationUpdate(BaseModel):
    maximum_payload: Decimal | None = Field(default=None, gt=0)
    baggage_capacity: Decimal | None = Field(default=None, ge=0)
    configured_by: UUID | None = None


class AircraftOperationalConfigurationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    aircraft_id: UUID
    maximum_payload: Decimal
    baggage_capacity: Decimal
    configured_by: UUID | None
    config_at: datetime
    updated_at: datetime
