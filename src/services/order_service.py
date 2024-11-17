import smtplib
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO

from fastapi import HTTPException

from sqlalchemy.orm import Session

from src.repositories.order import generate_pdf_receipt, get_order_by_id, saving_receipt, update_services, \
    book_schedule_slot, check_office_availability, create_order, get_orders_by_client_id
from src.schemas.order_schemas import OrderRequest


def create_order_service(db: Session, order_data: OrderRequest):
    existing_orders = check_office_availability(db, order_data.office_id, order_data.duration)

    if len(existing_orders) >= 3:
        raise HTTPException(status_code=406, detail='The office is not available for the requested duration. Maximum of 3 overlapping orders allowed.')
    book_schedule_slot(db, order_data.office_id, order_data.duration)
    return create_order(db, order_data)

def update_order_service(db: Session, order_id:int, order_data: OrderRequest):
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