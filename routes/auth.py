from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi import Request
from auth.rate_limit import limiter

from database import SessionLocal
from models.admin import Admin

from schemas.auth import (
    AdminRegister,
    AdminLogin,
    RefreshTokenRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    # create_password_reset_token,
    
)

from auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    create_password_reset_token
)

from auth.dependencies import get_current_admin


router = APIRouter(
    prefix="/auth",
    tags=["Admin Login"]
)


# ============================================================
# DATABASE DEPENDENCY
# ============================================================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ============================================================
# 1. ADMIN REGISTER
# ============================================================

@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def register_admin(
    request: Request,
    data: AdminRegister,
    db: Session = Depends(get_db)
):    

    
    # CHECK EXISTING EMAIL
    existing_email = (
        db.query(Admin)
        .filter(Admin.email == data.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin email already registered"
        )

    # CHECK EXISTING MOBILE NUMBER
    existing_mobile = (
        db.query(Admin)
        .filter(Admin.mobile_number == data.mobile_number)
        .first()
    )

    if existing_mobile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mobile number already registered"
        )


    # --------------------------------------------------------
    # HASH PASSWORD
    # --------------------------------------------------------

    hashed_password = hash_password(
        data.password
    )

    # --------------------------------------------------------
    # CREATE ADMIN
    # --------------------------------------------------------

    admin = Admin(
        full_name=data.full_name,
        email=data.email,
        mobile_number=data.mobile_number,
        password_hash=hashed_password,
        role="ADMIN",
        is_active=True
    )

    db.add(admin)

    db.commit()

    db.refresh(admin)

    return {
        "message": "Admin registered successfully",
        "admin": {
            "id": admin.id,
            "full_name": admin.full_name,
            "email": admin.email,
            "mobile_number": admin.mobile_number,
            "role": admin.role,
            "is_active": admin.is_active
        }
    }


# ============================================================
# 2. ADMIN LOGIN
# ============================================================

@router.post("/login")
@limiter.limit("5/minute")
def login_admin(
    request: Request,
    data: AdminLogin,
    db: Session = Depends(get_db)
):  

    # --------------------------------------------------------
    # FIND ADMIN
    # --------------------------------------------------------

    admin = (
        db.query(Admin)
        .filter(
            Admin.email == data.email
        )
        .first()
    )

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # --------------------------------------------------------
    # VERIFY PASSWORD
    # --------------------------------------------------------

    if not verify_password(
        data.password,
        admin.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # --------------------------------------------------------
    # CHECK ACTIVE STATUS
    # --------------------------------------------------------

    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin account is inactive"
        )

    # --------------------------------------------------------
    # CREATE TOKENS
    # --------------------------------------------------------

    access_token = create_access_token(
        admin_id=admin.id,
        email=admin.email,
        role=admin.role
    )

    refresh_token = create_refresh_token(
        admin_id=admin.id
    )

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {
        "message": "Admin login successful",
        "token_type": "bearer",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in_minutes": 30,
        "admin": {
            "id": admin.id,
            "full_name": admin.full_name,
            "email": admin.email,
            "mobile_number": admin.mobile_number,
            "role": admin.role
        }
    }


# ============================================================
# 3. REFRESH ACCESS TOKEN
# ============================================================

@router.post("/refresh")
def refresh_access_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a new access token
    using a valid refresh token.
    """

    # --------------------------------------------------------
    # DECODE REFRESH TOKEN
    # --------------------------------------------------------

    try:
        payload = decode_token(
            data.refresh_token
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    # --------------------------------------------------------
    # CHECK TOKEN TYPE
    # --------------------------------------------------------

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # --------------------------------------------------------
    # GET ADMIN ID
    # --------------------------------------------------------

    admin_id = payload.get("sub")

    if not admin_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # --------------------------------------------------------
    # FIND ADMIN
    # --------------------------------------------------------

    admin = (
        db.query(Admin)
        .filter(
            Admin.id == (admin_id)
        )
        .first()
    )

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin not found"
        )

    # --------------------------------------------------------
    # CHECK ACTIVE STATUS
    # --------------------------------------------------------

    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin account is inactive"
        )

    # --------------------------------------------------------
    # CREATE NEW ACCESS TOKEN
    # --------------------------------------------------------

    access_token = create_access_token(
        admin_id=admin.id,
        email=admin.email,
        role=admin.role
    )

    return {
        "message": "Access token refreshed successfully",
        "token_type": "bearer",
        "access_token": access_token,
        "expires_in_minutes": 30
    }


# ============================================================
# 4. FORGOT PASSWORD
# ============================================================

@router.post("/forgot-password")
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    admin = db.query(Admin).filter(
        Admin.email == data.email
    ).first()

    if not admin:
        return {
            "message": "If this email is registered, password reset instructions will be sent."
        }

    reset_token = create_password_reset_token(admin.id)

    return {
        "message": "Password reset token generated successfully",
        "reset_token": reset_token
    }

    # --------------------------------------------------------
    # GENERIC RESPONSE
    # --------------------------------------------------------
    # We don't reveal whether the email exists.

    return {
        "message": (
            "If this email is registered, "
            "password reset instructions will be sent."
        )
    }



@router.post("/reset-password")
def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    from auth.security import decode_token, hash_password
    from models.admin import Admin
    from fastapi import HTTPException, status

    if data.new_password != data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and confirm password do not match"
        )

    try:
        payload = decode_token(data.access_token)

        # Accept only tokens specifically created for password reset.
        if payload.get("type") != "password_reset":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password reset token"
            )

        admin_id = int(payload.get("sub"))

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired password reset token"
        )

    admin = db.query(Admin).filter(Admin.id == admin_id).first()

    if not admin or not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin account not found or inactive"
        )

    admin.password_hash = hash_password(data.new_password)
    db.commit()

    return {"message": "Password reset successfully"}

# ============================================================
# 5. GET CURRENT ADMIN PROFILE
# ============================================================

@router.get("/me")
def get_current_admin_profile(
    admin: Admin = Depends(get_current_admin)
):
    """
    Return the currently authenticated Admin profile.
    """

    return {
        "message": "Authenticated Admin",
        "data": {
            "id": admin.id,
            "full_name": admin.full_name,
            "email": admin.email,
            "mobile_number": admin.mobile_number,
            "role": admin.role,
            "is_active": admin.is_active,
            "created_at": admin.created_at
        }
    }