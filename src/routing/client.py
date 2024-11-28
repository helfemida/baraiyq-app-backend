from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from starlette.responses import StreamingResponse

from src.database import get_db
from src.repositories.clients import get_client_by_id
from src.schemas.office_schemas import Feedbacks
from src.schemas.order_schemas import OrderRequest, OrderResponse
from src.services.offices_service import get_offices_info, get_single_office, create_feedback, search_offices_service

from src.schemas.auth_schemas import SignUpRequest
from src.services.auth_service import authenticate_client_phone, authenticate_client_email, verify_signup
from src.schemas.auth_schemas import SignInEmailRequest, SignInPhoneRequest
from src.services.order_service import create_order_service, get_orders_by_client_id_service, get_order_by_id, \
    update_order_service, cancel_order_service, generate_receipt_service, send_email

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

@router.get("/offices/search/")
def search_office(
        name: str = Query(..., description="Search term for the office name"),
    db: Session = Depends(get_db)
):
    return search_offices_service(db, name)

@router.get("/offices/{office_id}/")
def read_offices(office_id: int, db: Session = Depends(get_db)):
    return JSONResponse(get_single_office(office_id, db))

@router.post("/offices/feedbacks/post/")
def submit_feedback(feedback: Feedbacks, db: Session = Depends(get_db)):
    return JSONResponse(create_feedback(db, feedback))

@router.post("/order/{office_id}/", response_model=OrderResponse)
def place_order(order: OrderRequest, db: Session = Depends(get_db)):
    return create_order_service(db, order)

@router.get("/orders/{client_id}/", response_model=List[OrderResponse])
def get_client_orders(client_id: int, db: Session = Depends(get_db)):
    return get_orders_by_client_id_service(db, client_id)

@router.get("/orders/order/{order_id}/", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return get_order_by_id(db, order_id)

@router.put("/order/update/{order_id}/", response_model=OrderResponse)
def update_order(order_id: int, order: OrderRequest, db: Session = Depends(get_db)):
    return update_order_service(db, order_id, order)

@router.delete("/order/cancel/{order_id}/")
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    cancel_order_service(order_id, db)
    return {"message": f"Order {order_id} cancelled successfully"}

@router.get("/order/payment/{order_id}/")
def generate_receipt(order_id: int, db: Session = Depends(get_db)):
    pdf_file = generate_receipt_service(order_id, db)

    return StreamingResponse(
        pdf_file,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=receipt_{order_id}.pdf"}
    )

@router.get("/orders/payment/email/{order_id}/")
def send_receipt_email(order_id: int, db: Session = Depends(get_db)):
    order = get_order_by_id(db, order_id)

    subject = f"Your Receipt for Order #{order_id}"
    c = get_client_by_id(db, order.client_id)
    recipient = c.email
    content = f"Dear {c.name},\n\nThank you for your payment.\n\n"
    content += f"Order ID: {order_id}\nTotal: ${order.total_sum}\nDate: {order.duration}\n\n"
    content += "Here is your receipt:"
    pdf_receipt = generate_receipt_service(order_id, db)
    send_email(recipient, subject, content, pdf_receipt)
    return JSONResponse(status_code=200, content={"message": "Receipt sent successfully"})
