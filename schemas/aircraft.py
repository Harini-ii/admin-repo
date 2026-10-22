
from uuid import UUID
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AircraftCreate(BaseModel):
    model: str = Field(min_length=1, max_length=100)
    type: Literal["FLIGHT", "HELICOPTER"]
    seating: int = Field(gt=0)


class AircraftUpdate(BaseModel):
    model: str | None = Field(default=None, min_length=1, max_length=100)
    type: Literal["FLIGHT", "HELICOPTER"] | None = None
    seating: int | None = Field(default=None, gt=0)


class AircraftResponse(BaseModel):
    id: UUID
    model: str
    type: str
    seating: int
    image: str | None = None
    maximum_payload: float | None = None
    baggage_capacity: float | None = None

    model_config = ConfigDict(from_attributes=True)


class AircraftImageResponse(BaseModel):
    id: UUID
    aircraft_id: UUID
    model: str
    capacity: int
    seats: int
    created_at: datetime
    image_url: str

    model_config = ConfigDict(from_attributes=True)

class AircraftLimitsCreate(BaseModel):
    maximum_payload: float = Field(ge=0)
    baggage_capacity: float = Field(ge=0)