from datetime import datetime
from io import BytesIO

from fastapi import HTTPException
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session, joinedload

from src.models import Order, OrderService, Receipt
from src.repositories import order
from src.schemas.order_schemas import OrderRequest


def create_order_service(db: Session, order_data: OrderRequest):
    existing_orders = order.check_office_availability(db, order_data.office_id, order_data.duration)

    if len(existing_orders) >= 3:
        raise HTTPException(status_code=406, detail='The office is not available for the requested duration. Maximum of 3 overlapping orders allowed.')
    order.book_schedule_slot(db, order_data.office_id, order_data.duration)
    return order.create_order(db, order_data)

def get_orders_by_client_id(db: Session, client_id: int):
    return db.query(Order).options(joinedload(Order.services)).filter(Order.client_id == client_id).all()

def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).options(joinedload(Order.services)).filter(Order.id == order_id).first()

def update_order_service(db: Session, order_id:int, order_data: OrderRequest):
    order = db.query(Order).filter(Order.id == order_id).first()
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

    db.query(OrderService).filter(OrderService.order_id == order_id).delete()
    for service in order_data.services:
        new_service = OrderService(order_id=order_id, service_name=service.service_name)
        db.add(new_service)

    db.commit()
    db.refresh(order)
    return order

def cancel_order_service(order_id: int, db: Session):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = "Cancelled"
    db.commit()

def generate_pdf_receipt(order_data):
    # Create a buffer to store the PDF in memory
    buffer = BytesIO()

    # Create a canvas object to draw on the PDF
    c = canvas.Canvas(buffer, pagesize=letter)

    # Set up basic styles for the invoice
    c.setFont("Helvetica", 12)

    # Draw a title (Invoice/Receipt)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "Invoice / Receipt")

    # Draw company name and contact information
    c.setFont("Helvetica", 12)
    c.drawString(30, 730, "Baraiyq.kz")
    c.drawString(30, 715, "1/1 Abylaikhan Street, Kaskelen, 040900 Almaty, Kazakhstan")
    c.drawString(30, 700, "Email: baraiyq@gmail.com")
    c.drawString(30, 685, "Phone: +7778 777 77 77")

    # Draw the receipt information
    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, 730, f"Receipt No: {order_data['receipt_number']}")
    c.drawString(400, 715, f"Date: {order_data['created_at']}")

    # Draw order details
    c.setFont("Helvetica", 12)
    c.drawString(30, 640, f"Order ID: {order_data['order_id']}")
    c.drawString(30, 625, f"Client ID: {order_data['client_id']}")
    c.drawString(30, 610, f"Office Name: {order_data['office_name']}")
    c.drawString(30, 595, f"Address: {order_data['address']}")
    c.drawString(30, 580, f"Order Status: {order_data['status'].name}")
    c.drawString(30, 565, f"Total Amount: ${order_data['total_sum']:.2f}")

    # Draw services section
    c.drawString(30, 540, "Services:")
    y_position = 525
    for service in order_data['services']:
        c.drawString(30, y_position, f"- {service['service_name']}")
        y_position -= 15

    # Draw a line separator
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)

    # Add footer with the "thank you" message
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(30, 100, "Thank you for your business!")

    # Finalize the PDF
    c.showPage()
    c.save()

    # Move buffer cursor to the beginning and return the PDF data
    buffer.seek(0)
    return buffer  # Return PDF as a BytesIO object




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

    receipt = Receipt(
        order_id=order.id,
        receipt_number=receipt_data["receipt_number"],
        total_sum=order.total_sum,
    )
    db.add(receipt)
    db.commit()

    pdf_file = generate_pdf_receipt(receipt_data)

    return pdf_file