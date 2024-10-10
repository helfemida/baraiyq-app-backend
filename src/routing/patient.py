from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.schemas.auth_schemas import VerificationRequest, SignUpRequest, SignInRequest
from src.services.auth_service import send_verification_code
from src.database import get_db
from src.schemas.doctor_schemas import DoctorOut
from src.services.doctor_service import get_doctors
from typing import List, Optional
from fastapi.responses import JSONResponse
from src.services.auth_service import authenticate_patient, verify_signup
from src.services.resource_service import get_resources

router = APIRouter()

@router.post("/auth/sign-up")
def signup(request: SignUpRequest, db: Session = Depends(get_db)):
    token = verify_signup(db, request, request.emailVerificationCode)
    return JSONResponse(
        content={"message": "Signup successful"},
        headers={"Auth": token}
    )


@router.post("/auth/sign-in")
def login_patient(request: SignInRequest, db: Session = Depends(get_db)):
    token = authenticate_patient(db, request)
    return JSONResponse(
        content={"message": "Login successful"},
        headers={"Auth": token},
        status_code=200
    )