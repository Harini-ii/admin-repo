
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.admin import Admin
from models.operation_profile import OperationProfile
from models.operators_profile import OperatorsProfile

from auth.dependencies import get_current_admin
from auth.team_dependencies import get_current_team_user
from auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    create_password_reset_token,
    decode_token,
)

from schemas.team_profiles import (
    TeamProfileCreate,
    TeamProfileUpdate,
    TeamLogin,
    TeamRefreshToken,
    TeamForgotPassword,
    TeamResetPassword,
    TeamChangePassword,
    TeamProfileResponse,
)
from fastapi import FastAPI

app = FastAPI(
    title="Puspakavimanam Aviation Management API"
)

operations_router = APIRouter(
    prefix="/operations",
    tags=["Operations Profile"],
)

operators_router = APIRouter(
    prefix="/operators",
    tags=["Operators Profile"],
)




def create_profile_routes(router, model, role):
    # ADMIN ONLY: Create an account
    @router.post(
        "/register",
        response_model=TeamProfileResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def create_account(
        data: TeamProfileCreate,
        db: Session = Depends(get_db),
        admin: Admin = Depends(get_current_admin),
    ):
        email = data.email.lower()

        if db.query(model).filter(model.email == email).first():
            raise HTTPException(status_code=409, detail="Email already exists")

        if db.query(model).filter(
            model.phone_number == data.phone_number
        ).first():
            raise HTTPException(status_code=409, detail="Phone number already exists")

        account = model(
            full_name=data.full_name,
            email=email,
            phone_number=data.phone_number,
            password_hash=hash_password(data.password),
            role=role,
            is_active=True,
        )

        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    # Login
    @router.post("/login")
    def login(data: TeamLogin, db: Session = Depends(get_db)):
        account = db.query(model).filter(
            model.email == data.email.lower()
        ).first()

        if not account or not verify_password(
            data.password, account.password_hash
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password",
            )

        if not account.is_active:
            raise HTTPException(status_code=403, detail="Account is inactive")

        return {
            "message": "Login successful",
            "access_token": create_access_token(
                admin_id=account.id,
                email=account.email,
                role=role,
            ),
            "refresh_token": create_refresh_token(admin_id=account.id),
            "token_type": "bearer",
            "user": {
                "id": str(account.id),
                "full_name": account.full_name,
                "email": account.email,
                "phone_number": account.phone_number,
                "role": role,
            },
        }

    # Refresh access token
    @router.post("/refresh")
    def refresh_token(
        data: TeamRefreshToken,
        db: Session = Depends(get_db),
    ):
        try:
            payload = decode_token(data.refresh_token)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Refresh token required")

        if payload.get("role") != role:
            raise HTTPException(status_code=403, detail="Token role mismatch")

        try:
            account_id = uuid.UUID(str(payload.get("sub")))
        except (ValueError, TypeError, AttributeError):
            raise HTTPException(status_code=401, detail="Invalid account ID")

        account = db.query(model).filter(model.id == account_id).first()

        if not account or not account.is_active:
            raise HTTPException(status_code=401, detail="Account not found or inactive")

        return {
            "access_token": create_access_token(
                admin_id=account.id,
                email=account.email,
                role=role,
            ),
            "refresh_token": create_refresh_token(admin_id=account.id),
            "token_type": "bearer",
        }

    # Forgot password
    @router.post("/forgot-password")
    def forgot_password(
        data: TeamForgotPassword,
        db: Session = Depends(get_db),
    ):
        account = db.query(model).filter(
            model.email == data.email.lower()
        ).first()

        response = {
            "message": "If the account exists, password reset instructions will be provided."
        }

        if account:
            # Development/testing only. In production, email this token
            # through a secure, short-lived password-reset link.
            response["reset_token"] = create_password_reset_token(account.id)

        return response

    # Reset password using a password-reset token
    @router.post("/reset-password")
    def reset_password(
        data: TeamResetPassword,
        db: Session = Depends(get_db),
    ):
        try:
            payload = decode_token(data.reset_token)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid or expired reset token")

        if payload.get("type") != "password_reset":
            raise HTTPException(status_code=401, detail="Password reset token required")

        try:
            account_id = uuid.UUID(str(payload.get("sub")))
        except (ValueError, TypeError, AttributeError):
            raise HTTPException(status_code=401, detail="Invalid account ID")

        account = db.query(model).filter(model.id == account_id).first()

        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        account.password_hash = hash_password(data.new_password)
        db.commit()

        return {"message": "Password reset successfully"}

    # Change password for the logged-in team member
    @router.post("/change-password")
    def change_password(
        data: TeamChangePassword,
        db: Session = Depends(get_db),
        account=Depends(get_current_team_user),
    ):
        if account.role != role:
            raise HTTPException(status_code=403, detail="Wrong team account")

        if not verify_password(data.current_password, account.password_hash):
            raise HTTPException(status_code=400, detail="Current password is incorrect")

        if data.current_password == data.new_password:
            raise HTTPException(
                status_code=400,
                detail="New password must differ from current password",
            )

        account.password_hash = hash_password(data.new_password)
        db.commit()

        return {"message": "Password changed successfully"}

    # ADMIN ONLY: Get all accounts
    @router.get("/", response_model=list[TeamProfileResponse])
    def get_all_accounts(
        db: Session = Depends(get_db),
        admin: Admin = Depends(get_current_admin),
    ):
        return db.query(model).order_by(model.created_at.desc()).all()

    # ADMIN ONLY: Get account by UUID
    @router.get("/{account_id}", response_model=TeamProfileResponse)
    def get_account(
        account_id: uuid.UUID,
        db: Session = Depends(get_db),
        admin: Admin = Depends(get_current_admin),
    ):
        account = db.query(model).filter(model.id == account_id).first()

        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        return account

    # ADMIN ONLY: Update account details
    @router.put("/{account_id}", response_model=TeamProfileResponse)
    def update_account(
        account_id: uuid.UUID,
        data: TeamProfileUpdate,
        db: Session = Depends(get_db),
        admin: Admin = Depends(get_current_admin),
    ):
        account = db.query(model).filter(model.id == account_id).first()

        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        updates = data.model_dump(exclude_unset=True)

        for field, value in updates.items():
            if value is None:
                continue

            if field == "email":
                value = value.lower()
                existing = db.query(model).filter(
                    model.email == value,
                    model.id != account_id,
                ).first()
                if existing:
                    raise HTTPException(status_code=409, detail="Email already exists")

            if field == "phone_number":
                existing = db.query(model).filter(
                    model.phone_number == value,
                    model.id != account_id,
                ).first()
                if existing:
                    raise HTTPException(
                        status_code=409,
                        detail="Phone number already exists",
                    )

            setattr(account, field, value)

        db.commit()
        db.refresh(account)
        return account

    # ADMIN ONLY: Delete account
    @router.delete("/{account_id}")
    def delete_account(
        account_id: uuid.UUID,
        db: Session = Depends(get_db),
        admin: Admin = Depends(get_current_admin),
    ):
        account = db.query(model).filter(model.id == account_id).first()

        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        db.delete(account)
        db.commit()

        return {"message": f"{role} account deleted successfully"}


create_profile_routes(operations_router, OperationProfile, "OPERATIONS")
create_profile_routes(operators_router, OperatorsProfile, "OPERATOR")
app.include_router(operations_router)
app.include_router(operators_router)
