from datetime import datetime, timedelta, timezone

from jose import jwt
from pwdlib import PasswordHash
from schemas.auth import (
    AdminRegister,
    AdminLogin,
    RefreshTokenRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)



# ============================================
# PASSWORD HASHING
# ============================================

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Convert a plain-text password into a secure hash.
    """
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify a plain-text password against its stored hash.
    """
    return password_hash.verify(
        plain_password,
        hashed_password
    )


# ============================================
# JWT CONFIGURATION
# ============================================

SECRET_KEY = "change-this-secret-key-later"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

REFRESH_TOKEN_EXPIRE_DAYS = 7


# ============================================
# CREATE ACCESS TOKEN
# ============================================

def create_access_token(
    admin_id: int,
    email: str,
    role: str
) -> str:

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(admin_id),
        "email": email,
        "role": role,
        "type": "access",
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# ============================================
# CREATE REFRESH TOKEN
# ============================================

def create_refresh_token(
    admin_id: int
) -> str:

    expire = datetime.now(timezone.utc) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload = {
        "sub": str(admin_id),
        "type": "refresh",
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# ============================================
# DECODE JWT TOKEN
# ============================================

def decode_token(token: str):

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )
def create_password_reset_token(admin_id):
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    payload = {
        "sub": str(admin_id),
        "type": "password_reset",
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )