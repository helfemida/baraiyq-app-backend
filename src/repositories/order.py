import string
from datetime import datetime
from io import BytesIO
from typing import List

from sqlalchemy import cast, Date, Time
from sqlalchemy.orm import Session, joinedload
from src.models import Order, OrderService, ScheduleSlot, Receipt
from src.repositories.managers import assign_manager, get_last_assigned_manager
from src.schemas.order_schemas import OrderRequest
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_order(db: Session, order_data: OrderRequest):
    last_manager_id = get_last_assigned_manager(db)
    next_manager_id = assign_manager(last_manager_id)

    db_order = Order(
        office_id=order_data.office_id,
        client_id=order_data.client_id,
        manager_id = next_manager_id,
        office_name=order_data.office_name,
        office_desc=order_data.office_desc,
        address=order_data.address,
        max_capacity=order_data.max_capacity,
        duration=order_data.duration,
        status=order_data.status,
        total_sum=order_data.total_sum
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for service in order_data.services:
        db_service = OrderService(order_id=db_order.id, service_name=service.service_name)
        db.add(db_service)

    db.commit()
    return db_order

def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).options(joinedload(Order.services)).filter(Order.id == order_id).first()

def get_orders_by_client_id(db: Session, client_id: int):
    return db.query(Order).options(joinedload(Order.services)).filter(Order.client_id == client_id).all()

def parse_func(duration: str):
    date, time_range = duration.split(" ")
    start_time, end_time = time_range.split("-")
    start_datetime = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
    end_datetime = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")
    return start_datetime, end_datetime


def check_office_availability(db: Session, office_id: int, duration: str):
    start_datetime, end_datetime = parse_func(duration)

    available_slots = db.query(ScheduleSlot).filter(
        ScheduleSlot.office_id == office_id,
        ScheduleSlot.is_booked == False,
        cast(ScheduleSlot.day, Date) == start_datetime.date(),
        cast(ScheduleSlot.start_time, Time) >= start_datetime.time(),
        cast(ScheduleSlot.end_time, Time) <= end_datetime.time()
    ).all()

    return available_slots


def book_schedule_slot(db: Session, office_id: int, duration: str):
    date, time_range = duration.split(" ")
    start_time, end_time = time_range.split("-")

    schedule_slot = db.query(ScheduleSlot).filter(
        ScheduleSlot.office_id == office_id,
        ScheduleSlot.day == date,
        ScheduleSlot.start_time == start_time,
        ScheduleSlot.end_time == end_time
    ).first()

    if schedule_slot:
        schedule_slot.is_booked = True
        db.commit()

def update_services(db: Session, order_id: int, order_data: OrderRequest):
    db.query(OrderService).filter(OrderService.order_id == order_id).delete()
    for service in order_data.services:
        new_service = OrderService(order_id=order_id, service_name=service.service_name)
        db.add(new_service)

def saving_receipt(db: Session, receipt_num:string, order: OrderRequest):

    receipt = Receipt(
        order_id=order.id,
        receipt_number=receipt_num,
        total_sum=order.total_sum,
    )
    db.add(receipt)
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