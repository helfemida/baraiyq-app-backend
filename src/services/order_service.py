import smtplib
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO

from fastapi import HTTPException

from sqlalchemy.orm import Session

from src.models import Order, Manager, Client
from src.repositories.order import generate_pdf_receipt, get_order_by_id, saving_receipt, update_services, \
    book_schedule_slot, check_office_availability, create_order, get_orders_by_client_id, get_orders_by_manager_id, \
    get_all_orders, get_manager_by_order_id
from src.repositories.schedules import create_schedule
from src.schemas.office_schemas import OfficeResponse
from src.schemas.order_schemas import OrderRequest, OrderStatusRequest, OrderByManagerResponse, OrderServiceResponse
from src.schemas.schedule_schemas import ScheduleRequest
from src.repositories.clients import get_client_by_id
from src.repositories.managers import get_admin_privelegy_by_manager_id, get_manager_by_id
from src.repositories.offices import get_office_by_id


def create_order_service(db: Session, order_data: OrderRequest):
    existing_orders = check_office_availability(db, order_data.office_id, order_data.duration)

    if len(existing_orders) >= 3:
        raise HTTPException(status_code=406,
                            detail='The office is not available for the requested duration. Maximum of 3 overlapping orders allowed.')
    book_schedule_slot(db, order_data.office_id, order_data.duration)
    return create_order(db, order_data)


def update_order_service(db: Session, order_id: int, order_data: OrderRequest):
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.office_id = order_data.office_id
    order.client_id = order_data.client_id
    order.office_name = order_data.office_name
    order.office_desc = order_data.office_desc
    order.address = order_data.address
    order.max_capacity = order_data.max_capacity
    order.duration = order_data.duration
    order.status = order_data.status
    order.total_sum = order_data.total_sum

    update_services(db, order_id, order_data)

    db.commit()
    db.refresh(order)
    return order


def get_orders_by_client_id_service(db: Session, client_id: int):
    return get_orders_by_client_id(db, client_id)


def cancel_order_service(order_id: int, db: Session):
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = "Cancelled"
    db.commit()


def generate_receipt_service(order_id: int, db: Session):
    order = get_order_by_id(db, order_id)

    receipt_data = {
        "order_id": order.id,
        "receipt_number": f"REC{order.id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        "total_sum": order.total_sum,
        "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "client_id": order.client_id,
        "office_name": order.office_name,
        "address": order.address,
        "status": order.status,
        "services": [{"service_name": service.service_name} for service in order.services]
    }

    saving_receipt(db, receipt_data["receipt_number"], order)

    pdf_file = generate_pdf_receipt(receipt_data)

    return pdf_file


def send_email(to_address: str, subject: str, content: str, pdf_attachment: BytesIO):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "nuspekovalihan@gmail.com"
    sender_password = "sbwlgtbryqkgynvv"
    sender_name = "baraiyq.kz"

    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = f"{sender_name} <{sender_email}>"
    message["To"] = to_address

    message.attach(MIMEText(content, "plain"))

    pdf_attachment.seek(0)
    pdf_part = MIMEApplication(pdf_attachment.read(), _subtype="pdf")
    pdf_part.add_header('Content-Disposition', 'attachment', filename="receipt.pdf")
    message.attach(pdf_part)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_address, message.as_string())
    except Exception as e:
        print("Failed to send email:", e)
        raise


def get_all_orders_by_privelegy(manager_id: int, db: Session):
    if get_admin_privelegy_by_manager_id(db, manager_id):
        return get_all_orders(db)
    else:
        return HTTPException(status_code=402, detail="Forbidden")


def get_orders_managers(manager_id: int, db: Session):
    if get_admin_privelegy_by_manager_id(db, manager_id):
        return toJsonSerializable(get_all_orders(db), db)
    elif get_orders_by_manager_id(db, manager_id):
        return toJsonSerializable(get_orders_by_manager_id(db, manager_id), db)
    else:
        return HTTPException(status_code=404, detail="No orders found")


def toJsonSerializable(db_orders: list[Order], db: Session):
    all_orders = []

    for order in db_orders:
        db_client = get_client_by_id(db, order.client_id)
        db_manager = get_manager_by_id(db, order.manager_id)
        db_office = get_office_by_id(db, order.office_id)
        services = []

        for service in order.services:
            dict_service = {
                "id": service.id,
                "service_name": service.service_name
            }
            services.append(dict_service)

        order_dict = {
            "id": order.id,
            "client_id": db_client.id,
            "client_name": db_client.name,
            "client_surname": db_client.surname,
            "client_phone": db_client.phone,
            "client_email": db_client.email,
            "manager_id": db_manager.id,
            "manager_name": db_manager.name,
            "manager_surname": db_manager.surname,
            "office_id": db_office.get("id"),
            "office_name": db_office.get("name"),
            "office_desc": db_office.get("description"),
            "address": db_office.get("address"),
            "max_capacity": db_office.get("capacity"),
            "duration": order.duration,
            "status": order.status,
            "total_sum": order.total_sum,
            "services": services
        }
        all_orders.append(order_dict)

    return all_orders


def create_schedule_service(office_id: int, db: Session, request: ScheduleRequest):
    return create_schedule(db, office_id, request)


def update_order_status_service(db: Session, request: OrderStatusRequest):
    order = get_order_by_id(db, request.id)
    order.status = request.status
    db.commit()
    db.refresh(order)
