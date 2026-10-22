# ```python
from pydantic import BaseModel, EmailStr, Field, field_validator

def validate_password_strength(password: str) -> str:
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not any(char.isupper() for char in password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not any(char.islower() for char in password):
        raise ValueError("Password must contain at least one lowercase letter")
    if not any(char.isdigit() for char in password):
        raise ValueError("Password must contain at least one number")
    if not any(not char.isalnum() for char in password):
        raise ValueError("Password must contain at least one special character")
    return password


class AdminRegister(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    mobile_number: str = Field(min_length=10, max_length=15)
    password: str = Field(min_length=8, max_length=100)
    confirm_password: str = Field(min_length=8, max_length=100)

    @field_validator("password", "confirm_password")
    @classmethod
    def validate_password(cls, value: str):
        return validate_password_strength(value)


class AdminLogin(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(min_length=1)


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    access_token: str = Field(min_length=1)
    new_password: str = Field(min_length=8, max_length=100)
    confirm_password: str = Field(min_length=8, max_length=100)

    @field_validator("new_password", "confirm_password")
    @classmethod
    def validate_password(cls, value: str):
        return validate_password_strength(value)
# ```
