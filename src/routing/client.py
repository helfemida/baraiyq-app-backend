from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.orm import Session
from src.database import get_db
from fastapi.responses import JSONResponse
from src.services.auth_service import authenticate_patient, verify_signup
router = APIRouter()

@router.post("/auth/sign-up")
def signup(request: SignUpRequest, db: Session = Depends(get_db)):
    #add_client
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