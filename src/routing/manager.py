from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.order_schemas import OrderStatusRequest
from src.schemas.schedule_schemas import ScheduleRequest
from src.services.auth_service import authenticate_manager_email, authenticate_manager_phone
from src.schemas.auth_schemas import SignInEmailRequest, SignInPhoneRequest
from fastapi.responses import JSONResponse

from src.services.order_service import get_orders_managers, create_schedule_service, update_order_status_service

router = APIRouter()


@router.post("/auth/sign-in/email/")
def login_manager_email(request: SignInEmailRequest, db: Session = Depends(get_db)):
    token = authenticate_manager_email(db, request.email, request.password)
    if not token:
        return JSONResponse(content={"message": "Invalid credentials"}, status_code=401)

    headers = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET, POST, OPTIONS, PUT, DELETE"}
    content = {"message": "Login successful", "Auth": token}
    return JSONResponse(content=content, headers=headers)

@router.post("/auth/sign-in/phone/")
def login_manager_phone(request: SignInPhoneRequest, db: Session = Depends(get_db)):
    token = authenticate_manager_phone(db, request.phone, request.password)
    if not token:
        return JSONResponse(content={"message": "Invalid credentials"}, status_code=401)

    headers = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET, POST, OPTIONS, PUT, DELETE"}
    content = {"message": "Login successful", "Auth": token}
    return JSONResponse(content=content, headers=headers)

@router.get("/orders/{manager_id}/")
def get_orders(manager_id: int, db: Session = Depends(get_db)):
    orders = get_orders_managers(manager_id, db)
    return JSONResponse(content=orders, status_code=200)

@router.put("/orders/{order_id}/status/")
def update_order_status(request: OrderStatusRequest, db: Session = Depends(get_db)):
    update_order_status_service(db, request)
    return JSONResponse(content={"message": "Order status updated successfully"}, status_code=200)

@router.post("/create-schedule/{office_id}/")
def create_schedules(office_id: int, request: ScheduleRequest, db:Session = Depends(get_db)):
    schedule = create_schedule_service(office_id, db, request)
    return {"message": f"Schedule {schedule.id} created successfully!"}