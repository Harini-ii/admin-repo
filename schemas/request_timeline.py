
# schemas/request_timeline.py

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RequestTimelineFields(BaseModel):
    request_id: UUID
    actor_id: UUID | None = None
    event_type: str
    messages: str | None = None
    actor_role: str | None = None
    passenger_id: UUID | None = None
    passenger_document_id: UUID | None = None


class CustomerRequestTimelineCreate(RequestTimelineFields):
    pass


class SalesRequestTimelineCreate(RequestTimelineFields):
    pass


class CustomerRequestTimelineUpdate(BaseModel):
    actor_id: UUID | None = None
    event_type: str | None = None
    messages: str | None = None
    actor_role: str | None = None
    passenger_id: UUID | None = None
    passenger_document_id: UUID | None = None


class SalesRequestTimelineUpdate(CustomerRequestTimelineUpdate):
    pass


class RequestTimelineResponse(RequestTimelineFields):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime


class CustomerRequestTimelineResponse(RequestTimelineResponse):
    pass


class SalesRequestTimelineResponse(RequestTimelineResponse):
    pass


# Temporary compatibility with existing main.py imports.
# Update the endpoints to use Customer/Sales-specific schemas later.
RequestTimelineUpdate = CustomerRequestTimelineUpdate
