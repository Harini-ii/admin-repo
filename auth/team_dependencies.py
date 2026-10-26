
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import get_db
from auth.security import decode_token
from models.operation_profile import OperationProfile
from models.operators_profile import OperatorsProfile

security = HTTPBearer()

def get_current_team_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    try:
        payload = decode_token(credentials.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Access token required")

    subject = payload.get("sub")
    role = payload.get("role")

    try:
        user_id = uuid.UUID(str(subject))
    except (ValueError, TypeError, AttributeError):
        raise HTTPException(status_code=401, detail="Invalid account ID")

    if role == "OPERATIONS":
        model = OperationProfile
    elif role == "OPERATOR":
        model = OperatorsProfile
    else:
        raise HTTPException(status_code=403, detail="Invalid team role")

    user = db.query(model).filter(model.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="Account not found")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is inactive")

    return user
    