from pathlib import Path
import shutil
import uuid
from models.customer import Customer
from typing import Literal
from fastapi import (

          FastAPI,
          Depends,
          HTTPException,
          UploadFile,
          File,
          Form,
          status,
)


import uuid
import shutil
from pathlib import Path
from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, Query, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import get_db

from models.request import CustomerRequest, SalesRequest
from models.request_document import (
    CustomerRequestDocument,
    SalesRequestDocument,
)
from models.request_timeline import (
    CustomerRequestTimeline,
    SalesRequestTimeline,
)

from schemas.request import (
    CustomerRequestCreate,
    CustomerRequestUpdate,
    CustomerRequestResponse,
    SalesRequestCreate,
    SalesRequestUpdate,
    SalesRequestResponse,
)

from schemas.request_document import (
    CustomerRequestDocumentResponse,
    SalesRequestDocumentResponse,
)

from schemas.request_timeline import (
    CustomerRequestTimelineCreate,
    CustomerRequestTimelineUpdate,
    CustomerRequestTimelineResponse,
    SalesRequestTimelineCreate,
    SalesRequestTimelineUpdate,
    SalesRequestTimelineResponse,
)

from models.request import CustomerRequest, SalesRequest

from models.request_document import (
    CustomerRequestDocument,
    SalesRequestDocument,
)

from models.request_timeline import (
    CustomerRequestTimeline,
    SalesRequestTimeline,
)

from schemas.request import (
    CustomerRequestCreate,
    CustomerRequestUpdate,
    CustomerRequestResponse,
    SalesRequestCreate,
    SalesRequestUpdate,
    SalesRequestResponse,
)

from schemas.request_document import (
    CustomerRequestDocumentResponse,
    SalesRequestDocumentResponse,
)

from schemas.request_timeline import (
    CustomerRequestTimelineCreate,
    CustomerRequestTimelineUpdate,
    CustomerRequestTimelineResponse,
    SalesRequestTimelineCreate,
    SalesRequestTimelineUpdate,
    SalesRequestTimelineResponse,
)

from schemas.aircraft_operational_configuration import (
    AircraftOperationalConfigurationCreate,
    AircraftOperationalConfigurationUpdate,
    AircraftOperationalConfigurationResponse,
)
from schemas.request_timeline import (
    RequestTimelineUpdate,
    RequestTimelineResponse,
)
from schemas.aircraft import AircraftLimitsCreate
from uuid import UUID
from auth.dependencies import get_current_admin
from models.admin import Admin

from models.request_timeline import (
    CustomerRequestTimeline,
    SalesRequestTimeline,
)
from models.customer import Customer
from models.request import CustomerRequest, SalesRequest
from models.aircraft_opertional_configuration import AircraftOperationalConfiguration
from models.support import SupportTicket
from fastapi import Request as FastAPIRequest
from models.request_document import (
    CustomerRequestDocument,
    SalesRequestDocument,
)
from fastapi import HTTPException, Depends,Body
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal

# ============================================================
# MODELS
# ============================================================

from models.aircraft import Aircraft, AircraftImage
from models.sales_team import SalesTeam
from models.admin import Admin
from models.support import SupportTicket

# ============================================================
# SCHEMAS
# ============================================================
from schemas.aircraft import (
          AircraftCreate,
          AircraftUpdate,
)
from schemas.request import CustomerRequestUpdate, SalesRequestUpdate
from schemas.support import (

          SupportUpdate,

          SupportReply,

)



from slowapi.errors import RateLimitExceeded

from slowapi import _rate_limit_exceeded_handler

from auth.rate_limit import limiter





def validate_password_strength(password: str) -> str:

          if len(password) < 8:

                    raise HTTPException(

                              status_code=400,

                              detail="Password must be at least 8 characters long"

                    )



          if not any(char.isupper() for char in password):

                    raise HTTPException(

                              status_code=400,

                              detail="Password must contain at least one uppercase letter"

                    )



          if not any(char.islower() for char in password):

                    raise HTTPException(
                              status_code=400,
                              detail="Password must contain at least one lowercase letter"
                    )
          if not any(char.isdigit() for char in password):
                    raise HTTPException(
                              status_code=400,
                              detail="Password must contain at least one number"
                    )
          if not any(not char.isalnum() for char in password):
                    raise HTTPException(
                              status_code=400,
                              detail="Password must contain at least one special character"
                    )
          return password
AIRCRAFT_UPLOAD_DIR = Path("uploads/aircraft")
AIRCRAFT_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)\
# ============================================================
# AUTH
# ============================================================
from routes.auth import router as auth_router
from auth.security import hash_password
# ============================================================

# CREATE DATABASE TABLES

# ============================================================
# Base.metadata.create_all(bind=engine)

# ============================================================

# FASTAPI APP

# ============================================================
# from fastapi import FastAPI, Depends
# from fastapi.staticfiles import StaticFiles
# from auth.dependencies import get_current_admin
# app = FastAPI(

#           title="Aircraft & Sales Admin API",

#           version="1.0.0"

# )
# from fastapi import APIRouter, Depends

# from auth.dependencies import get_current_admin

# app = FastAPI(
#     title="Aircraft & Sales Admin API",
#     version="1.0.0"
# )

# # All routes registered on this router require a valid admin token.
# protected_router = APIRouter(
#     dependencies=[Depends(get_current_admin)]
# )

# # Keep authentication endpoints public.
# app.include_router(auth_router)


# from fastapi import APIRouter, Depends
# from auth.dependencies import get_current_admin

# protected_router = APIRouter(
#     dependencies=[Depends(get_current_admin)]
# )


from fastapi import FastAPI, Depends, APIRouter
from fastapi.staticfiles import StaticFiles
from auth.dependencies import get_current_admin
from routes.auth import router as auth_router

app = FastAPI(
    title="Aircraft & Sales Admin API",
    version="1.0.0",
)

# All business API endpoints require a valid admin access token.
protected_router = APIRouter(
    dependencies=[Depends(get_current_admin)]
)

# Authentication endpoints remain public, except /auth/me,
# which already has its own authentication dependency.
app.include_router(auth_router)


# ============================================================

# DATABASE DEPENDENCY

# ===================== =======================================



def get_db():

          db = SessionLocal()



          try:

                    yield db

          finally:

                    db.close()





# ============================================================

# ADMIN LOGIN / AUTH

# ============================================================



app.include_router(auth_router)





# ============================================================

# FILE UPLOAD DIRECTORY

# ============================================================



UPLOAD_DIR = Path("uploads/sales")



UPLOAD_DIR.mkdir(

          parents=True,

          exist_ok=True

)

# Serve uploaded files without adding a separate document API.
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")





# ============================================================

# ADMIN AIRCRAFT

# ============================================================





from typing import Literal





@protected_router.post(

          "/aircraft",

          tags=["Admin Aircraft"],

          status_code=status.HTTP_201_CREATED,

)

def create_aircraft(

          model: str = Form(..., min_length=1, max_length=100),

          type: Literal["FLIGHT", "HELICOPTER"] = Form(...),

          seating: int = Form(..., gt=0),

          image: UploadFile = File(..., description="Aircraft image"),

          db: Session = Depends(get_db),

):

          allowed_types = {"image/jpeg", "image/png", "image/webp"}

          allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}

          saved_file = None



          try:
                    filename = image.filename or ""
                    extension = Path(filename).suffix.lower()
                    if (
                              extension not in allowed_extensions
                              or image.content_type not in allowed_types

                    ):
                              raise HTTPException(
                                        status_code=status.HTTP_400_BAD_REQUEST,
                                        detail="Only JPG, JPEG, and WEBP image files are allowed"
                                        if False else
                                        "Only JPG, JPEG, PNG, and WEBP image files are allowed",
                              )
                    unique_filename = f"{uuid.uuid4().hex}{extension}"

                    file_path = AIRCRAFT_UPLOAD_DIR / unique_filename



                    # Save the uploaded image to disk.

                    with file_path.open("wb") as buffer:

                              shutil.copyfileobj(image.file, buffer)



                    saved_file = file_path

                    image_path = str(file_path).replace("\\\\", "/")



                    # Save aircraft details and the main image path.

                    new_aircraft = Aircraft(

                              model=model.strip(),

                              type=type,

                              seating=seating,

                              image=image_path,

                    )



                    db.add(new_aircraft)

                    db.commit()

                    db.refresh(new_aircraft)



                    return {

                              "message": "Aircraft created successfully",

                              "aircraft": {

                                        "id": new_aircraft.id,

                                        "model": new_aircraft.model,

                                        "type": new_aircraft.type,

                                        "seating": new_aircraft.seating,

                                        "image": new_aircraft.image,

                              },

                    }



          except HTTPException:

                    db.rollback()

                    if saved_file is not None:

                              saved_file.unlink(missing_ok=True)

                    raise

          except Exception:

                    db.rollback()

                    if saved_file is not None:

                              saved_file.unlink(missing_ok=True)

                    raise

          finally:

                    image.file.close()



@protected_router.post("/aircraft/{aircraft_id}/limits", tags=["Admin Aircraft"])
def create_aircraft_limits(
    aircraft_id: UUID,
    limits: AircraftLimitsCreate,
    db: Session = Depends(get_db),
):
    aircraft = (
        db.query(Aircraft)
        .filter(Aircraft.id == aircraft_id)
        .first()
    )

    if aircraft is None:
        raise HTTPException(
            status_code=404,
            detail="Aircraft not found",
        )

    aircraft.maximum_payload = limits.maximum_payload
    aircraft.baggage_capacity = limits.baggage_capacity

    try:
        db.commit()
        db.refresh(aircraft)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to save aircraft limits",
        )

    return {
        "message": "Aircraft limits saved successfully",
        "aircraft_id": str(aircraft.id),
        "maximum_payload": aircraft.maximum_payload,
        "baggage_capacity": aircraft.baggage_capacity,
    }

# ------------------------------------------------------------

# GET ALL AIRCRAFT + INVENTORY COUNTS

# ------------------------------------------------------------



@protected_router.get("/aircraft", tags=["Admin Aircraft"])

def get_all_aircraft(

          aircraft_type: str | None = None,

          search: str | None = None,

          db: Session = Depends(get_db),

):

          # Inventory counts from the complete database table

          total_count = db.query(Aircraft).count()

          flight_count = db.query(Aircraft).filter(

                    Aircraft.type == "FLIGHT"

          ).count()

          helicopter_count = db.query(Aircraft).filter(

                    Aircraft.type == "HELICOPTER"

          ).count()



          # Apply filters to the returned list

          query = db.query(Aircraft)



          if aircraft_type:

                    normalized_type = aircraft_type.strip().upper()



                    if normalized_type not in {"FLIGHT", "HELICOPTER"}:

                              raise HTTPException(

                                        status_code=400,

                                        detail="aircraft_type must be FLIGHT or HELICOPTER",

                              )



                    query = query.filter(Aircraft.type == normalized_type)



          if search and search.strip():

                    query = query.filter(

                              Aircraft.model.ilike(f"%{search.strip()}%")

                    )



          aircraft_list = query.order_by(Aircraft.id.desc()).all()



          return {

                    "count": len(aircraft_list),

                    "total_count": total_count,

                    "flight_count": flight_count,

                    "helicopter_count": helicopter_count,

                    "aircraft": aircraft_list,

          }







# ------------------------------------------------------------

# GET AIRCRAFT BY ID

# ------------------------------------------------------------



@protected_router.get(

          "/aircraft/{aircraft_id}",

          tags=["Admin Aircraft"],

)

def get_aircraft(

          aircraft_id: UUID,

          db: Session = Depends(get_db),

):

          aircraft = (

                    db.query(Aircraft)

                    .filter(

                              Aircraft.id == aircraft_id

                    )

                    .first()

          )



          if not aircraft:

                    raise HTTPException(

                              status_code=status.HTTP_404_NOT_FOUND,

                              detail="Aircraft not found",

                    )



          return aircraft

class AircraftLimitsUpdate(BaseModel):

          maximum_payload: float = Field(ge=0)

          baggage_capacity: float = Field(ge=0)



@protected_router.put("/aircraft/{aircraft_id}/limits", tags=["Admin Aircraft"])

def update_aircraft_limits(

          aircraft_id: UUID,

          limits: AircraftLimitsUpdate,

          db: Session = Depends(get_db),

):

          aircraft = (

                    db.query(Aircraft)

                    .filter(Aircraft.id == aircraft_id)

                    .first()

          )



          if not aircraft:

                    raise HTTPException(

                              status_code=404,

                              detail="Aircraft not found",

                    )



          aircraft.maximum_payload = limits.maximum_payload

          aircraft.baggage_capacity = limits.baggage_capacity



          db.commit()

          db.refresh(aircraft)



          return {

                    "message": "Aircraft operational limits updated successfully",

                    "aircraft": {

                              "id": aircraft.id,

                              "model": aircraft.model,

                              "maximum_payload": aircraft.maximum_payload,

                              "baggage_capacity": aircraft.baggage_capacity,

                    },

          }





# ------------------------------------------------------------

# UPDATE AIRCRAFT

# ------------------------------------------------------------



@protected_router.put(

          "/aircraft/{aircraft_id}",

          tags=["Admin Aircraft"],

)

def update_aircraft(

          aircraft_id: UUID,

          aircraft_data: AircraftUpdate,

          db: Session = Depends(get_db),

):

          aircraft = (

                    db.query(Aircraft)

                    .filter(

                              Aircraft.id == aircraft_id

                    )

                    .first()

          )



          if not aircraft:

                    raise HTTPException(

                              status_code=status.HTTP_404_NOT_FOUND,

                              detail="Aircraft not found",

                    )



          update_data = aircraft_data.model_dump(

                    exclude_unset=True

          )



          for key, value in update_data.items():

                    setattr(

                              aircraft,

                              key,

                              value

                    )



          db.commit()



          db.refresh(aircraft)



          return {

                    "message": "Aircraft updated successfully",

                    "aircraft": aircraft,

          }





# ------------------------------------------------------------

# BULK DELETE AIRCRAFT

# ------------------------------------------------------------



@protected_router.delete("/aircraft/bulk", tags=["Admin Aircraft"])

def delete_selected_aircraft(

          aircraft_ids: list[UUID] = Body(..., embed=True),

          db: Session = Depends(get_db),

):

          if not aircraft_ids:

                    raise HTTPException(

                              status_code=400,

                              detail="Select at least one aircraft",

                    )



          if any(aircraft_id <= 0 for aircraft_id in aircraft_ids):

                    raise HTTPException(
                              status_code=400,
                              detail="Aircraft IDs must be positive integers",
                    )

          unique_ids = list(set(aircraft_ids))
          aircraft_list = (

                    db.query(Aircraft)
                    .filter(Aircraft.id.in_(unique_ids))
                    .all()
          )
          found_ids = {aircraft.id for aircraft in aircraft_list}
          missing_ids = sorted(set(unique_ids) - found_ids)
          if missing_ids:

                    raise HTTPException(

                              status_code=404,

                              detail={"message": "Some aircraft were not found",

                                                  "missing_ids": missing_ids},

                    )

          try:
                    for aircraft in aircraft_list:

                              db.delete(aircraft)
                    db.commit()
                    return {

                              "message": "Selected aircraft deleted successfully",

                              "deleted_count": len(aircraft_list),

                              "deleted_ids": unique_ids,

                    }

          except Exception:

                    db.rollback()

                    raise
# ------------------------------------------------------------
# DELETE AIRCRAFT
# ------------------------------------------------------------

@protected_router.delete(
          "/aircraft/{aircraft_id}",
          tags=["Admin Aircraft"],
)
def delete_aircraft(
          aircraft_id: UUID,
          db: Session = Depends(get_db),
):
          aircraft = (
                    db.query(Aircraft)
                    .filter(
                              Aircraft.id == aircraft_id
                    )
                    .first()
          )
          if not aircraft:

                    raise HTTPException(

                              status_code=status.HTTP_404_NOT_FOUND,

                              detail="Aircraft not found",

                    )



          db.delete(aircraft)



          db.commit()



          return {

                    "message": "Aircraft deleted successfully"

          }


# GET: Retrieve aircraft operational configuration
@protected_router.get(
    "/aircraft/{aircraft_id}/operational-configuration",
    response_model=AircraftOperationalConfigurationResponse,
    tags=["Admin Aircraft"],
)
def get_aircraft_configuration(
    aircraft_id: UUID,
    db: Session = Depends(get_db),
):
    configuration = (
        db.query(AircraftOperationalConfiguration)
        .filter(
            AircraftOperationalConfiguration.aircraft_id == aircraft_id
        )
        .first()
    )

    if not configuration:
        raise HTTPException(
            status_code=404,
            detail="Aircraft operational configuration not found",
        )

    return configuration


# PUT: Update aircraft operational configuration
@protected_router.put(
    "/aircraft/{aircraft_id}/operational-configuration",
    response_model=AircraftOperationalConfigurationResponse,
    tags=["Admin Aircraft"],
)
def update_aircraft_configuration(
    aircraft_id: UUID,
    data: AircraftOperationalConfigurationUpdate,
    db: Session = Depends(get_db),
):
    configuration = (
        db.query(AircraftOperationalConfiguration)
        .filter(
            AircraftOperationalConfiguration.aircraft_id == aircraft_id
        )
        .first()
    )

    if not configuration:
        raise HTTPException(
            status_code=404,
            detail="Aircraft operational configuration not found",
        )

    updates = data.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update",
        )

    for field, value in updates.items():
        setattr(configuration, field, value)

    db.commit()
    db.refresh(configuration)

    return configuration


# DELETE: Delete aircraft operational configuration
@protected_router.delete(
    "/aircraft/{aircraft_id}/operational-configuration",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Admin Aircraft"],
)
def delete_aircraft_configuration(
    aircraft_id: UUID,
    db: Session = Depends(get_db),
):
    configuration = (
        db.query(AircraftOperationalConfiguration)
        .filter(
            AircraftOperationalConfiguration.aircraft_id == aircraft_id
        )
        .first()
    )

    if not configuration:
        raise HTTPException(
            status_code=404,
            detail="Aircraft operational configuration not found",
        )

    db.delete(configuration)
    db.commit()

    return None


# ============================================================

# ADMIN CUSTOMERS

# ============================================================





# ------------------------------------------------------------

# GET ALL CUSTOMERS

# ------------------------------------------------------------





@protected_router.get(

          "/customers",

          tags=["Admin Customers"],

)

def get_all_customers(

          search: str | None = None,

          db: Session = Depends(get_db),

):

          query = db.query(Customer)



          # Search by customer name, email, or phone number

          if search:

                    search_value = f"%{search}%"



                    query = query.filter(

                              (Customer.name.ilike(search_value))

                              | (Customer.email.ilike(search_value))

                              | (Customer.phone_number.ilike(search_value))

                    )



          # Get all customers, newest first

          customers = (

                    query

                    .order_by(Customer.created_at.desc())

                    .all()

          )



          return {

                    "count": len(customers),

                    "customers": [

                              {

                                        "customer_id": customer.customer_id,

                                        "name": customer.name,

                                        "email": customer.email,

                                        "phone_number": customer.phone_number,

                                        "created_at": customer.created_at,

                              }

                              for customer in customers

                    ],

          }



# --------------------------------------------------------

# GET ALL CUSTOMERS

# --------------------------------------------------------



@protected_router.get("/customers", tags=["Admin Customers"])

def get_customers(db: Session = Depends(get_db)):



          customers = (

                    db.query(Customer)

                    .order_by(Customer.created_at.desc())

                    .all()

          )



          return {

                    "count": len(customers),

                    "customers": [

                              {

                                        "customer_id": customer.customer_id,

                                        "name": customer.name,

                                        "email": customer.email,

                                        "phone_number": customer.phone_number,

                                        "created_at": customer.created_at,

                              }

                              for customer in customers

                    ],

          }





# --------------------------------------------------------

# GET CUSTOMER BY ID

# --------------------------------------------------------



@protected_router.get(

          "/customers/{customer_id}",

          tags=["Admin Customers"],

)

def get_customer(

          customer_id: UUID,

          db: Session = Depends(get_db),

):

          customer = (

                    db.query(Customer)

                    .filter(Customer.customer_id == customer_id)

                    .first()

          )



          if not customer:

                    raise HTTPException(

                              status_code=status.HTTP_404_NOT_FOUND,

                              detail="Customer not found",

                    )



          return {

                    "customer_id": customer.customer_id,

                    "name": customer.name,

                    "email": customer.email,

                    "phone_number": customer.phone_number,

                    "created_at": customer.created_at,

          }

# ============================================================

# SALES TEAM

# ============================================================



# IMPORTANT:

# Sales Team CREATE uses Form() and File()

# because Identity Document is an actual file upload.

#

# We DO NOT use SalesTeamCreate here.

#

# The database stores the FILE PATH as a string.

# The actual document is saved inside:

#

# uploads/sales/

#

# ============================================================





# ------------------------------------------------------------

# CREATE SALES MEMBER

# ------------------------------------------------------------



@protected_router.post(

          "/sales-team",

          tags=["Sales Team"],

          status_code=status.HTTP_201_CREATED

)

def create_sales_member(

          full_name: str = Form(...),

          email: str = Form(...),

          password: str = Form(...),

          mobile_number: str = Form(...),

          department: str = Form(...),

          notes: str | None = Form(None),

          identity_document: UploadFile | None = File(None),

          request: FastAPIRequest = None,

          db: Session = Depends(get_db),



):

          # Check if email already exists

          existing_member = db.query(SalesTeam).filter(

                    SalesTeam.email == email

          ).first()



          if existing_member:

                    raise HTTPException(

                              status_code=400,

                              detail="Sales team member with this email already exists"

                    )



          # PASSWORD VALIDATION

          validate_password_strength(password)



          # Hash password AFTER validation

          hashed_password = hash_password(password)



          # Identity document upload

          identity_document_path = None

          identity_document_url = None



          if identity_document:

                    if not identity_document.filename:

                              raise HTTPException(

                                        status_code=400,

                                        detail="Invalid identity document"

                              )



                    extension = Path(identity_document.filename).suffix.lower()



                    unique_filename = (

                              f"{uuid.uuid4().hex}{extension}"

                    )



                    file_path = UPLOAD_DIR / unique_filename



                    with file_path.open("wb") as buffer:

                              shutil.copyfileobj(

                                        identity_document.file,

                                        buffer

                              )



                    identity_document_path = file_path.as_posix()

                    identity_document_url = (
                              str(request.base_url).rstrip("/")
                              + "/uploads/sales/" + unique_filename
                    )



          # Create sales team member

          new_member = SalesTeam(

                    full_name=full_name,

                    email=email,

                    password_hash=hashed_password,

                    mobile_number=mobile_number,

                    department=department,

                    notes=notes,

                    identity_document=identity_document_path,

                    url=identity_document_url,

          )



          db.add(new_member)

          db.commit()

          db.refresh(new_member)



          return {

                    "message": "Sales team member created successfully",

                    "sales_member": new_member

          }

# ------------------------------------------------------------

# GET ALL SALES MEMBERS

# ------------------------------------------------------------



@protected_router.get(

          "/sales-team",

          tags=["Sales Team"],

)

def get_all_sales_members(

          db: Session = Depends(get_db),

):

          members = (

                    db.query(SalesTeam)

                    .order_by(

                              SalesTeam.id.desc()

                    )

                    .all()

          )



          return {

                    "count": len(members),

                    "sales_team": [

                              {

                                        "id": member.id,

                                        "full_name": member.full_name,

                                        "email": member.email,

                                        "mobile_number": member.mobile_number,

                                        "department": member.department,

                                        "notes": member.notes,

                                        "identity_document": member.identity_document,

                                        "joined_at": member.joined_at,
        "url": member.url,
        "created_at": member.created_at,
        "updated_at": member.updated_at,
                "url": member.url,
                "created_at": member.created_at,
                "updated_at": member.updated_at,

                              }

                              for member in members

                    ],

          }





# ------------------------------------------------------------

# GET SALES MEMBER BY ID

# ------------------------------------------------------------



@protected_router.get(

          "/sales-team/{member_id}",

          tags=["Sales Team"],

)

def get_sales_member(

          member_id: UUID,

          db: Session = Depends(get_db),

):

          member = (

                    db.query(SalesTeam)

                    .filter(

                              SalesTeam.id == member_id

                    )

                    .first()

          )



          if not member:

                    raise HTTPException(

                              status_code=status.HTTP_404_NOT_FOUND,

                              detail="Sales member not found",

                    )



          return {

                    "id": member.id,

                    "full_name": member.full_name,

                    "email": member.email,

                    "mobile_number": member.mobile_number,

                    "department": member.department,

                    "notes": member.notes,

                    "identity_document": member.identity_document,

                    "joined_at": member.joined_at,

                    "url": member.url,

                    "created_at": member.created_at,

                    "updated_at": member.updated_at,

          }





# ------------------------------------------------------------

# UPDATE SALES MEMBER

# ------------------------------------------------------------



@protected_router.put(

          "/sales-team/{member_id}",

          tags=["Sales Team"],

)

def update_sales_member(

          member_id: UUID,

          full_name: str | None = Form(None),

          email: str | None = Form(None),

          password: str | None = Form(None),

          mobile_number: str | None = Form(None),

          department: str | None = Form(None),

          notes: str | None = Form(None),

          identity_document: UploadFile | None = File(None),

          request: FastAPIRequest = None,

          db: Session = Depends(get_db),

):



          member = (

                    db.query(SalesTeam)

                    .filter(

                              SalesTeam.id == member_id

                    )

                    .first()

          )



          if not member:

                    raise HTTPException(

                              status_code=status.HTTP_404_NOT_FOUND,

                              detail="Sales member not found",

                    )



          # --------------------------------------------------------

          # UPDATE FULL NAME

          # --------------------------------------------------------



          if full_name is not None:

                    member.full_name = full_name



          # --------------------------------------------------------

          # UPDATE EMAIL

          # --------------------------------------------------------



          if email is not None:



                    existing_email = (

                              db.query(SalesTeam)

                              .filter(

                                        SalesTeam.email == email,

                                        SalesTeam.id != member_id,

                              )

                              .first()

                    )



                    if existing_email:

                              raise HTTPException(

                                        status_code=status.HTTP_400_BAD_REQUEST,

                                        detail="Email already exists",

                              )



                    member.email = email



          # --------------------------------------------------------

          # UPDATE PASSWORD

          # --------------------------------------------------------



          if password is not None:

                    member.password_hash = (

                              hash_password(password)

                    )



          # --------------------------------------------------------

          # UPDATE MOBILE

          # --------------------------------------------------------



          if mobile_number is not None:

                    member.mobile_number = mobile_number



          # --------------------------------------------------------

          # UPDATE DEPARTMENT

          # --------------------------------------------------------



          if department is not None:

                    member.department = department



          # --------------------------------------------------------

          # UPDATE NOTES

          # --------------------------------------------------------



          if notes is not None:

                    member.notes = notes



          # --------------------------------------------------------

          # UPDATE IDENTITY DOCUMENT

          # --------------------------------------------------------



          if identity_document:



                    original_filename = (

                              identity_document.filename

                    )



                    if not original_filename:

                              raise HTTPException(

                                        status_code=status.HTTP_400_BAD_REQUEST,

                                        detail="Invalid identity document",

                              )



                    extension = Path(

                              original_filename

                    ).suffix.lower()



                    unique_filename = (

                              f"{uuid.uuid4().hex}"

                              f"{extension}"

                    )



                    file_path = (

                              UPLOAD_DIR /

                              unique_filename

                    )



                    with file_path.open("wb") as buffer:



                              shutil.copyfileobj(

                                        identity_document.file,

                                        buffer

                              )



                    member.identity_document = file_path.as_posix()

                    member.url = (
                              str(request.base_url).rstrip("/")
                              + "/uploads/sales/" + unique_filename
                    )



          # --------------------------------------------------------

          # SAVE

          # --------------------------------------------------------



          db.commit()



          db.refresh(member)



          return {

                    "message": "Sales member updated successfully",

                    "sales_member": {

                              "id": member.id,

                              "full_name": member.full_name,

                              "email": member.email,

                              "mobile_number": member.mobile_number,

                              "department": member.department,

                              "notes": member.notes,

                              "identity_document": member.identity_document,

                              "joined_at": member.joined_at,

                              "url": member.url,

                              "created_at": member.created_at,

                              "updated_at": member.updated_at,

                    },

          }





# ------------------------------------------------------------

# DELETE SALES MEMBER

# ------------------------------------------------------------



@protected_router.delete(

          "/sales-team/{member_id}",

          tags=["Sales Team"],

)

def delete_sales_member(

          member_id: UUID,

          db: Session = Depends(get_db),

):

          member = (

                    db.query(SalesTeam)

                    .filter(

                              SalesTeam.id == member_id

                    )

                    .first()

          )



          if not member:

                    raise HTTPException(

                              status_code=status.HTTP_404_NOT_FOUND,

                              detail="Sales member not found",

                    )



          db.delete(member)



          db.commit()



          return {

                    "message": "Sales member deleted successfully"

          }





# ============================================================

# ADMIN REQUEST

# ============================================================



# Admin does NOT create requests.

#

# Requests come from Customer / Sales Team.

#

# Admin can:

# GET

# GET BY ID

# PATCH

# DELETE

#

# ============================================================



from uuid import UUID



# ------------------------------------------------------------

# GET ALL REQUESTS

# ------------------------------------------------------------



# @app.get(

#           "/requests",

#           tags=["Admin Request"],

# )

# def get_requests(

#           request_status: str | None = None,

#           request_type: str | None = None,

#           db: Session = Depends(get_db),

# ):

#           query = db.query(Request)



#           # Filter by status

#           if request_status:

#                     query = query.filter(

#                               Request.status == request_status.upper()

#                     )



#           # Filter by request type

#           if request_type:

#                     query = query.filter(

#                               Request.request_type == request_type.upper()

#                     )



#           # Sort newest requests first

#           requests = (

#                     query

#                     .order_by(Request.created_at.desc())

#                     .all()

#           )



#           return {

#                     "count": len(requests),

#                     "requests": requests,

#           }





# # ------------------------------------------------------------

# # GET REQUEST BY UUID

# # ------------------------------------------------------------



# @app.get(

#           "/requests/{request_id}",

#           tags=["Admin Request"],

# )

# def get_request(

#           request_id: UUID,

#           db: Session = Depends(get_db),

# ):

#           request_data = (

#                     db.query(Request)

#                     .filter(Request.id == request_id)

#                     .first()

#           )



#           if not request_data:

#                     raise HTTPException(

#                               status_code=status.HTTP_404_NOT_FOUND,

#                               detail="Request not found",

#                     )



#           return request_data





# # ------------------------------------------------------------

# # GET REQUEST CUSTOMER DETAILS

# # ------------------------------------------------------------



# @app.get(

#           "/requests/{request_id}/customer",

#           tags=["Admin Request"],

# )

# def get_request_customer_details(

#           request_id: UUID,

#           db: Session = Depends(get_db),

# ):

#           request_record = (

#                     db.query(Request)

#                     .filter(Request.id == request_id)

#                     .first()

#           )



#           if not request_record:

#                     raise HTTPException(

#                               status_code=status.HTTP_404_NOT_FOUND,

#                               detail="Request not found",

#                     )



#           return {

#                     "request_id": str(request_record.id),

#                     "request_number": request_record.request_number,

#                     "request_type": request_record.request_type,

#                     "status": request_record.status,



#                     "customer": {

#                               "customer_id": request_record.customer_id,

#                               "customer_name": request_record.customer_name,

#                               "customer_email": request_record.customer_email,

#                               "customer_mobile": request_record.customer_mobile,

#                     },



#                     "request_details": {

#                               "destination": request_record.destination,

#                               "identity_document": request_record.identity_document,

#                               "mode": request_record.mode,

#                               "access": request_record.access,

#                     },



#                     "created_at": request_record.created_at,

#                     "updated_at": request_record.updated_at,

#           }





# # ------------------------------------------------------------

# # UPDATE REQUEST

# # ------------------------------------------------------------



# @app.patch(

#           "/requests/{request_id}",

#           tags=["Admin Request"],

# )

# def update_request(

#           request_id: UUID,

#           request_data: RequestUpdate,

#           db: Session = Depends(get_db),

# ):

#           request_record = (

#                     db.query(Request)

#                     .filter(Request.id == request_id)

#                     .first()

#           )



#           if not request_record:

#                     raise HTTPException(

#                               status_code=status.HTTP_404_NOT_FOUND,

#                               detail="Request not found",

#                     )



#           update_data = request_data.model_dump(

#                     exclude_unset=True

#           )



#           for key, value in update_data.items():

#                     setattr(request_record, key, value)



#           try:

#                     db.commit()

#                     db.refresh(request_record)

#           except Exception:

#                     db.rollback()

#                     raise HTTPException(

#                               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

#                               detail="Failed to update request",

#                     )



#           return {

#                     "message": "Request updated successfully",

#                     "request": request_record,

#           }





# # ------------------------------------------------------------

# # DELETE REQUEST

# # ------------------------------------------------------------



# @app.delete(

#           "/requests/{request_id}",

#           tags=["Admin Request"],

# )

# def delete_request(

#           request_id: UUID,

#           db: Session = Depends(get_db),

# ):

#           request_record = (

#                     db.query(Request)

#                     .filter(Request.id == request_id)

#                     .first()

#           )



#           if not request_record:

#                     raise HTTPException(

#                               status_code=status.HTTP_404_NOT_FOUND,

#                               detail="Request not found",

#                     )



#           try:

#                     db.delete(request_record)

#                     db.commit()

#           except Exception:

#                     db.rollback()

#                     raise HTTPException(

#                               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

#                               detail="Failed to delete request",

#                     )



#           return {

#                     "message": "Request deleted successfully"

#           }

# # GET: Retrieve timeline entries for a request
# @app.get(
#     "/admin/requests/{request_id}/timeline",
#     response_model=list[RequestTimelineResponse],
#     tags=["Admin Request"],
# )
# def get_request_timeline(
#     request_id: UUID,
#     db: Session = Depends(get_db),
# ):
#     entries = (
#         db.query(RequestTimeline)
#         .filter(RequestTimeline.request_id == request_id)
#         .order_by(RequestTimeline.created_at.desc())
#         .all()
#     )

#     if not entries:
#         raise HTTPException(
#             status_code=404,
#             detail="No timeline entries found for this request",
#         )

#     return entries


# # PUT: Update a timeline entry
# @app.put(
#     "/admin/requests/{request_id}/timeline/{timeline_id}",
#     response_model=RequestTimelineResponse,
#     tags=["Admin Request"],
# )
# def update_request_timeline(
#     request_id: UUID,
#     timeline_id: UUID,
#     data: RequestTimelineUpdate,
#     db: Session = Depends(get_db),
# ):
#     entry = (
#         db.query(RequestTimeline)
#         .filter(
#             RequestTimeline.id == timeline_id,
#             RequestTimeline.request_id == request_id,
#         )
#         .first()
#     )

#     if not entry:
#         raise HTTPException(
#             status_code=404,
#             detail="Timeline entry not found",
#         )

#     for field, value in data.model_dump(exclude_unset=True).items():
#         setattr(entry, field, value)

#     db.commit()
#     db.refresh(entry)

#     return entry


# # DELETE: Delete a timeline entry
# @app.delete(
#     "/admin/requests/{request_id}/timeline/{timeline_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     tags=["Admin Request"],
# )
# def delete_request_timeline(
#     request_id: UUID,
#     timeline_id: UUID,
#     db: Session = Depends(get_db),
# ):
#     entry = (
#         db.query(RequestTimeline)
#         .filter(
#             RequestTimeline.id == timeline_id,
#             RequestTimeline.request_id == request_id,
#         )
#         .first()
#     )

#     if not entry:
#         raise HTTPException(
#             status_code=404,
#             detail="Timeline entry not found",
#         )

#     db.delete(entry)
#     db.commit()

#     return None



# ============================================================
# CUSTOMER REQUESTS
# ============================================================

@protected_router.post(
    "/customer-requests",
    response_model=CustomerRequestResponse,
    tags=["Customer Requests"],
)
def create_customer_request(
    payload: CustomerRequestCreate,
    db: Session = Depends(get_db),
):
    existing = (
        db.query(CustomerRequest)
        .filter(CustomerRequest.request_number == payload.request_number)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Customer request number already exists",
        )

    request = CustomerRequest(**payload.model_dump())
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


@protected_router.get(
    "/customer-requests",
    response_model=list[CustomerRequestResponse],
    tags=["Customer Requests"],
)
def list_customer_requests(
    status: Optional[str] = Query(default=None),
    request_type: Optional[str] = Query(default=None),
    customer_id: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(CustomerRequest)

    if status:
        query = query.filter(CustomerRequest.status.ilike(status))
    if request_type:
        query = query.filter(CustomerRequest.request_type.ilike(request_type))
    if customer_id:
        query = query.filter(CustomerRequest.customer_id == customer_id)

    return query.order_by(CustomerRequest.created_at.desc()).all()


@protected_router.get(
    "/customer-requests/{request_id}",
    response_model=CustomerRequestResponse,
    tags=["Customer Requests"],
)
def get_customer_request(
    request_id: UUID,
    db: Session = Depends(get_db),
):
    request = db.query(CustomerRequest).filter(
        CustomerRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(status_code=404, detail="Customer request not found")

    return request


@protected_router.get(
    "/customer-requests/{request_id}/customer",
    response_model=CustomerRequestResponse,
    tags=["Customer Requests"],
)
def get_customer_request_details(
    request_id: UUID,
    db: Session = Depends(get_db),
):
    request = db.query(CustomerRequest).filter(
        CustomerRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(status_code=404, detail="Customer request not found")

    return request


@protected_router.patch(
    "/customer-requests/{request_id}",
    response_model=CustomerRequestResponse,
    tags=["Customer Requests"],
)
def update_customer_request(
    request_id: UUID,
    payload: CustomerRequestUpdate,
    db: Session = Depends(get_db),
):
    request = db.query(CustomerRequest).filter(
        CustomerRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(status_code=404, detail="Customer request not found")

    updates = payload.model_dump(exclude_unset=True)

    if "request_number" in updates and updates["request_number"]:
        duplicate = (
            db.query(CustomerRequest)
            .filter(
                CustomerRequest.request_number == updates["request_number"],
                CustomerRequest.id != request_id,
            )
            .first()
        )
        if duplicate:
            raise HTTPException(
                status_code=409,
                detail="Customer request number already exists",
            )

    for field, value in updates.items():
        setattr(request, field, value)

    db.commit()
    db.refresh(request)
    return request


@protected_router.delete(
    "/customer-requests/{request_id}",
    tags=["Customer Requests"],
)
def delete_customer_request(
    request_id: UUID,
    db: Session = Depends(get_db),
):
    request = db.query(CustomerRequest).filter(
        CustomerRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(status_code=404, detail="Customer request not found")

    delete_request_documents(
        db,
        CustomerRequestDocument,
        request_id,
    )
    db.query(CustomerRequestTimeline).filter(
        CustomerRequestTimeline.request_id == request_id
    ).delete(synchronize_session=False)

    db.delete(request)
    db.commit()

    return {"message": "Customer request deleted successfully"}


# ============================================================
# SALES REQUESTS
# ============================================================

@protected_router.post(
    "/sales-requests",
    response_model=SalesRequestResponse,
    tags=["Sales Requests"],
)
def create_sales_request(
    payload: SalesRequestCreate,
    db: Session = Depends(get_db),
):
    existing = (
        db.query(SalesRequest)
        .filter(SalesRequest.request_number == payload.request_number)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Sales request number already exists",
        )

    request = SalesRequest(**payload.model_dump())
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


@protected_router.get(
    "/sales-requests",
    response_model=list[SalesRequestResponse],
    tags=["Sales Requests"],
)
def list_sales_requests(
    status: Optional[str] = Query(default=None),
    request_type: Optional[str] = Query(default=None),
    customer_id: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(SalesRequest)

    if status:
        query = query.filter(SalesRequest.status.ilike(status))
    if request_type:
        query = query.filter(SalesRequest.request_type.ilike(request_type))
    if customer_id:
        query = query.filter(SalesRequest.customer_id == customer_id)

    return query.order_by(SalesRequest.created_at.desc()).all()


@protected_router.get(
    "/sales-requests/{request_id}",
    response_model=SalesRequestResponse,
    tags=["Sales Requests"],
)
def get_sales_request(
    request_id: UUID,
    db: Session = Depends(get_db),
):
    request = db.query(SalesRequest).filter(
        SalesRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(status_code=404, detail="Sales request not found")

    return request


@protected_router.get(
    "/sales-requests/{request_id}/customer",
    response_model=SalesRequestResponse,
    tags=["Sales Requests"],
)
def get_sales_request_customer_details(
    request_id: UUID,
    db: Session = Depends(get_db),
):
    request = db.query(SalesRequest).filter(
        SalesRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(status_code=404, detail="Sales request not found")

    return request


@protected_router.patch(
    "/sales-requests/{request_id}",
    response_model=SalesRequestResponse,
    tags=["Sales Requests"],
)
def update_sales_request(
    request_id: UUID,
    payload: SalesRequestUpdate,
    db: Session = Depends(get_db),
):
    request = db.query(SalesRequest).filter(
        SalesRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(status_code=404, detail="Sales request not found")

    updates = payload.model_dump(exclude_unset=True)

    if "request_number" in updates and updates["request_number"]:
        duplicate = (
            db.query(SalesRequest)
            .filter(
                SalesRequest.request_number == updates["request_number"],
                SalesRequest.id != request_id,
            )
            .first()
        )
        if duplicate:
            raise HTTPException(
                status_code=409,
                detail="Sales request number already exists",
            )

    for field, value in updates.items():
        setattr(request, field, value)

    db.commit()
    db.refresh(request)
    return request


@protected_router.delete(
    "/sales-requests/{request_id}",
    tags=["Sales Requests"],
)
def delete_sales_request(
    request_id: UUID,
    db: Session = Depends(get_db),
):
    request = db.query(SalesRequest).filter(
        SalesRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(status_code=404, detail="Sales request not found")

    delete_request_documents(
        db,
        SalesRequestDocument,
        request_id,
    )
    db.query(SalesRequestTimeline).filter(
        SalesRequestTimeline.request_id == request_id
    ).delete(synchronize_session=False)

    db.delete(request)
    db.commit()

    return {"message": "Sales request deleted successfully"}



# ============================================================
# REQUEST DOCUMENT HELPERS
# ============================================================

UPLOAD_ROOT = Path(__file__).resolve().parent / "uploads"
MAX_UPLOAD_SIZE = 20 * 1024 * 1024  # 20 MB


def get_request_document_path(storage_path: str) -> Path:
    """Resolve a stored relative path and prevent paths outside uploads/."""
    root = UPLOAD_ROOT.resolve()
    path = (root / storage_path).resolve()

    if path != root and root not in path.parents:
        raise HTTPException(status_code=400, detail="Invalid document path")

    return path


def delete_request_documents(db: Session, document_model, request_id: UUID):
    documents = (
        db.query(document_model)
        .filter(document_model.request_id == request_id)
        .all()
    )

    for document in documents:
        try:
            path = get_request_document_path(document.storage_path)
            if path.is_file():
                path.unlink()
        except (OSError, HTTPException):
            pass

        db.delete(document)


def upload_request_document(
    db: Session,
    request_id: UUID,
    file: UploadFile,
    document_type: Optional[str],
    request_model,
    document_model,
    upload_subfolder: str,
):
    request = db.query(request_model).filter(
        request_model.id == request_id
    ).first()

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    original_filename = Path(file.filename or "upload").name
    contents = file.file.read()

    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    if len(contents) > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the 20 MB limit",
        )

    folder = UPLOAD_ROOT / upload_subfolder
    folder.mkdir(parents=True, exist_ok=True)

    saved_name = f"{uuid.uuid4().hex}_{original_filename}"
    destination = folder / saved_name
    destination.write_bytes(contents)

    relative_path = destination.relative_to(UPLOAD_ROOT).as_posix()

    # The request model currently stores customer_id as a string,
    # while the document model stores it as a UUID.
    customer_uuid = None
    try:
        customer_uuid = UUID(str(request.customer_id))
    except (ValueError, TypeError, AttributeError):
        pass

    document = document_model(
        request_id=request.id,
        customer_id=customer_uuid,
        storage_path=relative_path,
        original_filename=original_filename,
        mime_type=file.content_type,
        file_size=len(contents),
        document_type=document_type,
    )

    try:
        db.add(document)
        db.commit()
        db.refresh(document)
    except Exception:
        db.rollback()
        if destination.exists():
            destination.unlink()
        raise
    finally:
        file.file.close()

    return document


def list_request_documents(db: Session, request_id: UUID, request_model, document_model):
    request = db.query(request_model).filter(
        request_model.id == request_id
    ).first()

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    return (
        db.query(document_model)
        .filter(document_model.request_id == request_id)
        .order_by(document_model.created_at.desc())
        .all()
    )


def download_request_document(db: Session, document_id: UUID, document_model):
    document = db.query(document_model).filter(
        document_model.id == document_id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    path = get_request_document_path(document.storage_path)

    if not path.is_file():
        raise HTTPException(status_code=404, detail="Document file not found")

    return FileResponse(
        path=str(path),
        media_type=document.mime_type or "application/octet-stream",
        filename=document.original_filename,
    )


def remove_request_document(db: Session, document_id: UUID, document_model):
    document = db.query(document_model).filter(
        document_model.id == document_id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    path = get_request_document_path(document.storage_path)

    try:
        if path.is_file():
            path.unlink()
    except OSError as exc:
        raise HTTPException(
            status_code=500,
            detail="Could not delete the document file",
        ) from exc

    db.delete(document)
    db.commit()

    return {"message": "Document deleted successfully"}


# ============================================================
# CUSTOMER REQUEST DOCUMENTS
# ============================================================

@protected_router.post(
    "/customer-requests/{request_id}/documents",
    response_model=CustomerRequestDocumentResponse,
    tags=["Customer Request Documents"],
)
def upload_customer_request_document(
    request_id: UUID,
    file: UploadFile = File(...),
    document_type: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    return upload_request_document(
        db,
        request_id,
        file,
        document_type,
        CustomerRequest,
        CustomerRequestDocument,
        "customer-requests",
    )


@protected_router.get(
    "/customer-requests/{request_id}/documents",
    response_model=list[CustomerRequestDocumentResponse],
    tags=["Customer Request Documents"],
)
def list_customer_request_documents(
    request_id: UUID,
    db: Session = Depends(get_db),
):
    return list_request_documents(
        db, request_id, CustomerRequest, CustomerRequestDocument
    )


@protected_router.get(
    "/customer-request-documents/{document_id}/download",
    tags=["Customer Request Documents"],
)
def download_customer_request_document(
    document_id: UUID,
    db: Session = Depends(get_db),
):
    return download_request_document(db, document_id, CustomerRequestDocument)


@protected_router.delete(
    "/customer-request-documents/{document_id}",
    tags=["Customer Request Documents"],
)
def delete_customer_request_document(
    document_id: UUID,
    db: Session = Depends(get_db),
):
    return remove_request_document(db, document_id, CustomerRequestDocument)


# ============================================================
# SALES REQUEST DOCUMENTS
# ============================================================

@protected_router.post(
    "/sales-requests/{request_id}/documents",
    response_model=SalesRequestDocumentResponse,
    tags=["Sales Request Documents"],
)
def upload_sales_request_document(
    request_id: UUID,
    file: UploadFile = File(...),
    document_type: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    return upload_request_document(
        db,
        request_id,
        file,
        document_type,
        SalesRequest,
        SalesRequestDocument,
        "sales-requests",
    )


@protected_router.get(
    "/sales-requests/{request_id}/documents",
    response_model=list[SalesRequestDocumentResponse],
    tags=["Sales Request Documents"],
)
def list_sales_request_documents(
    request_id: UUID,
    db: Session = Depends(get_db),
):
    return list_request_documents(
        db, request_id, SalesRequest, SalesRequestDocument
    )


@protected_router.get(
    "/sales-request-documents/{document_id}/download",
    tags=["Sales Request Documents"],
)
def download_sales_request_document(
    document_id: UUID,
    db: Session = Depends(get_db),
):
    return download_request_document(db, document_id, SalesRequestDocument)


@protected_router.delete(
    "/sales-request-documents/{document_id}",
    tags=["Sales Request Documents"],
)
def delete_sales_request_document(
    document_id: UUID,
    db: Session = Depends(get_db),
):
    return remove_request_document(db, document_id, SalesRequestDocument)



# ============================================================
# CUSTOMER REQUEST TIMELINE
# ============================================================

@protected_router.post(
    "/customer-requests/{request_id}/timeline",
    response_model=CustomerRequestTimelineResponse,
    tags=["Customer Request Timeline"],
)
def create_customer_request_timeline(
    request_id: UUID,
    payload: CustomerRequestTimelineCreate,
    db: Session = Depends(get_db),
):
    request = db.query(CustomerRequest).filter(
        CustomerRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(status_code=404, detail="Customer request not found")

    if payload.request_id != request_id:
        raise HTTPException(
            status_code=400,
            detail="Timeline request_id must match the URL request_id",
        )

    timeline = CustomerRequestTimeline(**payload.model_dump())
    db.add(timeline)
    db.commit()
    db.refresh(timeline)
    return timeline


@protected_router.get(
    "/customer-requests/{request_id}/timeline",
    response_model=list[CustomerRequestTimelineResponse],
    tags=["Customer Request Timeline"],
)
def get_customer_request_timeline(
    request_id: UUID,
    db: Session = Depends(get_db),
):
    request = db.query(CustomerRequest).filter(
        CustomerRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(status_code=404, detail="Customer request not found")

    return (
        db.query(CustomerRequestTimeline)
        .filter(CustomerRequestTimeline.request_id == request_id)
        .order_by(CustomerRequestTimeline.created_at.asc())
        .all()
    )


@protected_router.patch(
    "/customer-requests/{request_id}/timeline/{timeline_id}",
    response_model=CustomerRequestTimelineResponse,
    tags=["Customer Request Timeline"],
)
def update_customer_request_timeline(
    request_id: UUID,
    timeline_id: UUID,
    payload: CustomerRequestTimelineUpdate,
    db: Session = Depends(get_db),
):
    timeline = (
        db.query(CustomerRequestTimeline)
        .filter(
            CustomerRequestTimeline.id == timeline_id,
            CustomerRequestTimeline.request_id == request_id,
        )
        .first()
    )

    if not timeline:
        raise HTTPException(status_code=404, detail="Customer timeline entry not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(timeline, field, value)

    db.commit()
    db.refresh(timeline)
    return timeline


@protected_router.delete(
    "/customer-requests/{request_id}/timeline/{timeline_id}",
    tags=["Customer Request Timeline"],
)
def delete_customer_request_timeline(
    request_id: UUID,
    timeline_id: UUID,
    db: Session = Depends(get_db),
):
    timeline = (
        db.query(CustomerRequestTimeline)
        .filter(
            CustomerRequestTimeline.id == timeline_id,
            CustomerRequestTimeline.request_id == request_id,
        )
        .first()
    )

    if not timeline:
        raise HTTPException(status_code=404, detail="Customer timeline entry not found")

    db.delete(timeline)
    db.commit()

    return {"message": "Customer request timeline entry deleted successfully"}


# ============================================================
# SALES REQUEST TIMELINE
# ============================================================

@protected_router.post(
    "/sales-requests/{request_id}/timeline",
    response_model=SalesRequestTimelineResponse,
    tags=["Sales Request Timeline"],
)
def create_sales_request_timeline(
    request_id: UUID,
    payload: SalesRequestTimelineCreate,
    db: Session = Depends(get_db),
):
    request = db.query(SalesRequest).filter(
        SalesRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(status_code=404, detail="Sales request not found")

    if payload.request_id != request_id:
        raise HTTPException(
            status_code=400,
            detail="Timeline request_id must match the URL request_id",
        )

    timeline = SalesRequestTimeline(**payload.model_dump())
    db.add(timeline)
    db.commit()
    db.refresh(timeline)
    return timeline


@protected_router.get(
    "/sales-requests/{request_id}/timeline",
    response_model=list[SalesRequestTimelineResponse],
    tags=["Sales Request Timeline"],
)
def get_sales_request_timeline(
    request_id: UUID,
    db: Session = Depends(get_db),
):
    request = db.query(SalesRequest).filter(
        SalesRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(status_code=404, detail="Sales request not found")

    return (
        db.query(SalesRequestTimeline)
        .filter(SalesRequestTimeline.request_id == request_id)
        .order_by(SalesRequestTimeline.created_at.asc())
        .all()
    )


@protected_router.patch(
    "/sales-requests/{request_id}/timeline/{timeline_id}",
    response_model=SalesRequestTimelineResponse,
    tags=["Sales Request Timeline"],
)
def update_sales_request_timeline(
    request_id: UUID,
    timeline_id: UUID,
    payload: SalesRequestTimelineUpdate,
    db: Session = Depends(get_db),
):
    timeline = (
        db.query(SalesRequestTimeline)
        .filter(
            SalesRequestTimeline.id == timeline_id,
            SalesRequestTimeline.request_id == request_id,
        )
        .first()
    )

    if not timeline:
        raise HTTPException(status_code=404, detail="Sales timeline entry not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(timeline, field, value)

    db.commit()
    db.refresh(timeline)
    return timeline


@protected_router.delete(
    "/sales-requests/{request_id}/timeline/{timeline_id}",
    tags=["Sales Request Timeline"],
)
def delete_sales_request_timeline(
    request_id: UUID,
    timeline_id: UUID,
    db: Session = Depends(get_db),
):
    timeline = (
        db.query(SalesRequestTimeline)
        .filter(
            SalesRequestTimeline.id == timeline_id,
            SalesRequestTimeline.request_id == request_id,
        )
        .first()
    )

    if not timeline:
        raise HTTPException(status_code=404, detail="Sales timeline entry not found")

    db.delete(timeline)
    db.commit()

    return {"message": "Sales request timeline entry deleted successfully"}




# ============================================================
# ADMIN SUPPORT
# ============================================================
# Customer creates support ticket.
# Admin only:
# GET
# GET BY ID
# PATCH
#
# Status:
# OPEN
# IN_PROGRESS
# RESOLVED
# CLOSED
# ------------------------------------------------------------
# GET ALL SUPPORT TICKETS
# ------------------------------------------------------------
@protected_router.get(

          "/support",

          tags=["Admin Support"],

)

def get_support_tickets(

          ticket_status: str | None = None,

          db: Session = Depends(get_db),

):



          query = db.query(

                    SupportTicket

          )



          if ticket_status:



                    query = query.filter(

                              SupportTicket.status ==

                              ticket_status.upper()

                    )



          tickets = (

                    query

                    .order_by(

                              SupportTicket.id.desc()

                    )

                    .all()

          )



          return {

                    "count": len(tickets),

                    "tickets": tickets,

          }





# ------------------------------------------------------------
# GET SUPPORT TICKET BY ID
# ------------------------------------------------------------



@protected_router.get(

          "/support/{ticket_id}",

          tags=["Admin Support"],

)

def get_support_ticket(

          ticket_id: UUID,

          db: Session = Depends(get_db),

):



          ticket = (

                    db.query(

                              SupportTicket

                    )

                    .filter(

                              SupportTicket.id == ticket_id

                    )

                    .first()

          )



          if not ticket:

                    raise HTTPException(

                              status_code=status.HTTP_404_NOT_FOUND,

                              detail="Support ticket not found",

                    )



          return ticket



@protected_router.post(

          "/support/{ticket_id}/reply",

          tags=["Admin Support"],

)

def reply_to_support_ticket(

          ticket_id: UUID,

          reply_data: SupportReply,

          db: Session = Depends(get_db),

):

          ticket = (

                    db.query(SupportTicket)

                    .filter(

                              SupportTicket.id == ticket_id

                    )

                    .first()

          )



          if not ticket:

                    raise HTTPException(

                              status_code=status.HTTP_404_NOT_FOUND,

                              detail="Support ticket not found",

                    )



          ticket.reply = reply_data.reply



          # Automatically move ticket to IN_PROGRESS

          # when admin replies

          if ticket.status == "OPEN":

                    ticket.status = "IN_PROGRESS"



          db.commit()

          db.refresh(ticket)



          return {

                    "message": "Reply sent successfully",

                    "ticket": ticket,

          }

# ------------------------------------------------------------

# UPDATE SUPPORT TICKET

# ------------------------------------------------------------



@protected_router.patch(

          "/support/{ticket_id}",

          tags=["Admin Support"],

)

def update_support_ticket(

          ticket_id: UUID,

          ticket_data: SupportUpdate,

          db: Session = Depends(get_db),

):



          ticket = (

                    db.query(

                              SupportTicket

                    )

                    .filter(

                              SupportTicket.id == ticket_id

                    )

                    .first()

          )



          if not ticket:

                    raise HTTPException(

                              status_code=status.HTTP_404_NOT_FOUND,

                              detail="Support ticket not found",

                    )



          update_data = (

                    ticket_data.model_dump(

                              exclude_unset=True

                    )

          )



          for key, value in update_data.items():



                    setattr(

                              ticket,

                              key,

                              value

                    )



          db.commit()



          db.refresh(ticket)



          return {

                    "message": "Support ticket updated successfully",

                    "ticket": ticket,

          }





# ============================================================

# CUSTOM SWAGGER / OPENAPI

# ============================================================

#

# IMPORTANT:

#

# This section ONLY changes how Swagger displays the API.

#

# It removes the red "\* required" markers.

#

# It DOES NOT remove FastAPI's actual validation.

#

# ============================================================





def custom_openapi():



          if app.openapi_schema:

                    return app.openapi_schema



          openapi_schema = get_openapi(

                    title=app.title,

                    version=app.version,

                    description=app.description,

                    routes=app.routes,

          )



          # --------------------------------------------------------

          # REQUEST BODIES

          # --------------------------------------------------------



          for path_data in openapi_schema.get(

                    "paths",

                    {}

          ).values():



                    for operation in path_data.values():



                              if not isinstance(

                                        operation,

                                        dict

                              ):

                                        continue



                              # ------------------------------------------------

                              # Request Body

                              # ------------------------------------------------



                              request_body = operation.get(

                                        "requestBody"

                              )



                              if request_body:



                                        # Remove red "required" for body

                                        request_body["required"] = False



                                        content = request_body.get(

                                                  "content",

                                                  {}

                                        )



                                        for media_type in content.values():



                                                  schema = media_type.get(

                                                            "schema"

                                                  )



                                                  if isinstance(

                                                            schema,

                                                            dict

                                                  ):



                                                            schema.pop(

                                                                      "required",

                                                                      None

                                                            )



                              # ------------------------------------------------

                              # Parameters

                              # ------------------------------------------------



                              parameters = operation.get(

                                        "parameters",

                                        []

                              )



                              for parameter in parameters:



                                        if isinstance(

                                                  parameter,

                                                  dict

                                        ):



                                                  parameter.pop(

                                                            "required",

                                                            None

                                                  )



          # --------------------------------------------------------

          # COMPONENT SCHEMAS

          # --------------------------------------------------------



          components = openapi_schema.get(

                    "components",

                    {}

          )



          schemas = components.get(

                    "schemas",

                    {}

          )



          for schema in schemas.values():



                    if isinstance(

                              schema,

                              dict

                    ):



                              # Remove required fields

                              schema.pop(

                                        "required",

                                        None

                              )



                              # Handle nested properties

                              properties = schema.get(

                                        "properties",

                                        {}

                              )



                              if isinstance(

                                        properties,

                                        dict

                              ):



                                        for property_data in properties.values():



                                                  if isinstance(

                                                            property_data,

                                                            dict

                                                  ):



                                                            property_data.pop(

                                                                      "required",

                                                                      None

                                                            )



                                                            # Swagger UI expects format="binary" to render a file picker.

                                                            # Newer FastAPI/Pydantic versions may emit contentMediaType instead.

                                                            if property_data.get("contentMediaType") == "application/octet-stream":

                                                                      property_data["format"] = "binary"

                                                                      property_data.pop("contentMediaType", None)



                                                            # Also handle arrays of uploaded files if another endpoint uses them.

                                                            items = property_data.get("items")

                                                            if isinstance(items, dict) and items.get("contentMediaType") == "application/octet-stream":

                                                                      items["format"] = "binary"

                                                                      items.pop("contentMediaType", None)



          app.openapi_schema = openapi_schema



          return app.openapi_schema





app.openapi = custom_openapi
# Register all protected business endpoints.
app.include_router(protected_router)

# Keep the existing custom Swagger/OpenAPI configuration.
app.openapi = custom_openapi