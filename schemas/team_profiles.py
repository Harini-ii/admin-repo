
import uuid
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)


# ---------------- PASSWORD VALIDATION ----------------

def validate_password_strength(password: str) -> str:
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")

    if not any(c.isupper() for c in password):
        raise ValueError("Password must contain an uppercase letter")

    if not any(c.islower() for c in password):
        raise ValueError("Password must contain a lowercase letter")

    if not any(c.isdigit() for c in password):
        raise ValueError("Password must contain a number")

    if not any(not c.isalnum() for c in password):
        raise ValueError("Password must contain a special character")

    return password


# ---------------- TEAM PROFILE CREATE ----------------

class TeamProfileCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone_number: str = Field(min_length=10, max_length=15)
    password: str = Field(min_length=8, max_length=100)
    confirm_password: str = Field(min_length=8, max_length=100)

    @field_validator("password", "confirm_password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password_strength(value)

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Password and confirm password do not match")
        return self


# ---------------- TEAM PROFILE UPDATE ----------------

class TeamProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(
        default=None, min_length=2, max_length=100
    )
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(
        default=None, min_length=10, max_length=15
    )
    is_active: Optional[bool] = None


# ---------------- TEAM LOGIN ----------------

class TeamLogin(BaseModel):
    email: EmailStr
    password: str


# ---------------- REFRESH TOKEN ----------------

class TeamRefreshToken(BaseModel):
    refresh_token: str = Field(min_length=1)


# ---------------- FORGOT PASSWORD ----------------

class TeamForgotPassword(BaseModel):
    email: EmailStr


# ---------------- RESET PASSWORD ----------------

class TeamResetPassword(BaseModel):
    reset_token: str = Field(min_length=1)
    new_password: str = Field(min_length=8, max_length=100)
    confirm_password: str = Field(min_length=8, max_length=100)

    @field_validator("new_password", "confirm_password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password_strength(value)

    @model_validator(mode="after")
    def passwords_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError("Password and confirm password do not match")
        return self


# ---------------- CHANGE PASSWORD ----------------

class TeamChangePassword(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=100)
    confirm_password: str = Field(min_length=8, max_length=100)

    @field_validator("new_password", "confirm_password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password_strength(value)

    @model_validator(mode="after")
    def passwords_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError("New password and confirm password do not match")
        return self


# ---------------- TEAM PROFILE RESPONSE ----------------

class TeamProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    full_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    role: str
    is_active: bool
