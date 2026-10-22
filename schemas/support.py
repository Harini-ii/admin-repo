from typing import Literal

from pydantic import BaseModel, Field

from typing import Literal
from pydantic import BaseModel, Field


class SupportUpdate(BaseModel):
    status: Literal[
        "OPEN",
        "IN_PROGRESS",
        "RESOLVED",
        "CLOSED"
    ] | None = None

    reply: str | None = Field(
        default=None,
        max_length=5000
    )


class SupportReply(BaseModel):
    reply: str = Field(
        min_length=1,
        max_length=5000
    )

class SupportUpdate(BaseModel):

    status: Literal[
        "OPEN",
        "IN_PROGRESS",
        "RESOLVED",
        "CLOSED"
    ] | None = None

    reply: str | None = Field(
        default=None,
        max_length=5000
    )
