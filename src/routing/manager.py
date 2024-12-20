from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.alternative_schemas import AlternativeResponseBase, AlternativeFilterRequest
from src.schemas.office_schemas import OfficeRequest, OfficeUpdateRequest
from src.schemas.order_schemas import OrderStatusRequest
from src.schemas.schedule_schemas import ScheduleRequest
from src.services.alternatives_service import get_all_alternatives_service, send_response_service, \
    get_all_alternatives_by_filter
from src.services.auth_service import authenticate_manager_email, authenticate_manager_phone
from src.schemas.auth_schemas import SignInEmailRequest, SignInPhoneRequest
from fastapi.responses import JSONResponse

from src.services.offices_service import create_office_service, update_office_by_id, delete_office_by_id
from src.services.order_service import get_orders_managers, create_schedule_service, update_order_status_service, \
    get_all_orders_by_privelegy

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
def create_schedules(office_id: int, request: ScheduleRequest, db: Session = Depends(get_db)):
    schedule = create_schedule_service(office_id, db, request)
    return {"message": f"Schedule {schedule.id} created successfully!"}


@router.post("/create-office/")
def create_office(request: OfficeRequest, db: Session = Depends(get_db)):
    office = create_office_service(db, request)
    return {"message": f"Office {office.id} created successfully!"}


@router.put("/update-office/")
def update_office(request: OfficeUpdateRequest, db: Session = Depends(get_db)):
    update_office_by_id(db, request)
    return JSONResponse(content=f"Office by id {id} is deleted successfully", status_code=200)


@router.delete("/delete-office/")
def delete_office(id: int, db: Session = Depends(get_db)):
    delete_office_by_id(db, id)
    return JSONResponse(content=f"Office by id {id} is deleted successfully", status_code=200)


@router.get("/alternative/requests/")
def get_alternatives_requests(db: Session = Depends(get_db)):
    alternatives = get_all_alternatives_service(db)
    return JSONResponse(content=alternatives, status_code=200)

@router.post("/alternative/requests/")
def get_alternatives_requests(request: AlternativeFilterRequest, db: Session = Depends(get_db)):
    alternatives = get_all_alternatives_by_filter(request, db)
    return JSONResponse(content=alternatives, status_code=200)


@router.post("/alternative/respond/{request_id}/")
def respond_to_request(request: AlternativeResponseBase, db: Session = Depends(get_db)):
    response = send_response_service(request, db)
    return JSONResponse(content={"message": f"Response {response.id} created successfully at {response.created_at}"},
                        status_code=200)
