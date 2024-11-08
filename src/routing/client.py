from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from src.database import get_db
from src.schemas.office_schemas import Feedbacks
from src.schemas.order_schemas import OrderRequest
from src.services.offices_service import get_offices_info, get_single_office, create_feedback

from src.schemas.auth_schemas import SignUpRequest
from src.services.auth_service import authenticate_client_phone, authenticate_client_email, verify_signup
from src.schemas.auth_schemas import SignInEmailRequest, SignInPhoneRequest
from src.services.order_service import create_order

router = APIRouter()


@router.post("/auth/sign-up/")
def signup(request: SignUpRequest, db: Session = Depends(get_db)):
    content = {"message": "Signup successful", "token": verify_signup(db, request)}
    return JSONResponse(content=content)


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


@router.get("/offices/")
def get_offices(db: Session = Depends(get_db)):
    return JSONResponse({"offices": get_offices_info(db)})

@router.get("/offices/{office_id}/")
def read_offices(office_id: int, db: Session = Depends(get_db)):
    return JSONResponse(get_single_office(office_id, db))

@router.post("/offices/feedbacks/post/")
def submit_feedback(feedback: Feedbacks, db: Session = Depends(get_db)):
    return JSONResponse(create_feedback(db, feedback))

@router.post("/orders/create/")
def place_order(order: OrderRequest, db: Session = Depends(get_db)):
    result = create_order(db, order)
    return JSONResponse(content=result)