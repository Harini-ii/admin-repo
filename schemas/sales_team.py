from pydantic import BaseModel, EmailStr, Field


class SalesTeamCreate(BaseModel):

    full_name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=100
    )

    mobile_number: str = Field(
        min_length=10,
        max_length=15
    )

    department: str = Field(
        min_length=2,
        max_length=100
    )

    notes: str | None = None

    identity_document: str | None = None


class SalesTeamUpdate(BaseModel):

    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    email: EmailStr | None = None

    mobile_number: str | None = Field(
        default=None,
        min_length=10,
        max_length=15
    )

    department: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    notes: str | None = None

    identity_document: str | None = None