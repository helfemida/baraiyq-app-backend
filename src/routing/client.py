from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.office_schemas import OfficeResponse
from src.services.office_service import get_available_offices

from src.schemas.auth_schemas import SignUpRequest
from src.services.auth_service import authenticate_client_phone, verify_signup
from src.schemas.auth_schemas import SignInEmailRequest, SignInPhoneRequest
router = APIRouter()

@router.post("/auth/sign-up/")
def signup(request: SignUpRequest, db: Session = Depends(get_db)):
    return verify_signup(db, request)


@router.post("/auth/sign-in/phone/")
def login_client(request: SignInPhoneRequest, db: Session = Depends(get_db)):
    token = authenticate_client_phone(db, request.phone, request.password)
    return {"message": "Login successful",
            "Auth": token}


@router.post("/auth/sign-in/email/")
def login_client(request: SignInEmailRequest, db: Session = Depends(get_db)):
    token = authenticate_client_phone(db, request.email, request.password)
    return {"message": "Login successful",
            "Auth": token}

@router.get("/offices/")
def read_offices(db: Session = Depends(get_db)) -> list[OfficeResponse]:
    offices = get_available_offices(db)
    return offices
