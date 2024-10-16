from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from src.database import get_db

from src.schemas.auth_schemas import SignUpRequest
from src.services.auth_service import authenticate_client_phone, authenticate_client_email, verify_signup
from src.schemas.auth_schemas import SignInEmailRequest, SignInPhoneRequest

router = APIRouter()


@router.post("/auth/sign-up/")
def signup(request: SignUpRequest, db: Session = Depends(get_db)):
    return verify_signup(db, request)


@router.post("/auth/sign-in/phone/")
def login_client_phone(request: SignInPhoneRequest, db: Session = Depends(get_db)):
    token = authenticate_client_phone(db, request.phone, request.password)
    headers = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET, POST, OPTIONS, PUT, DELETE"}
    content = {"message": "Login successful", "Auth": token}
    return JSONResponse(content=content, headers=headers)


@router.post("/auth/sign-in/email/")
def login_client_email(request: SignInEmailRequest, db: Session = Depends(get_db)):
    token = authenticate_client_email(db, request.email, request.password)
    headers = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET, POST, OPTIONS, PUT, DELETE"}
    content = {"message": "Login successful", "Auth": token}
    return JSONResponse(content=content, headers=headers)
