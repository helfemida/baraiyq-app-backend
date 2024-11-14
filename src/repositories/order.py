from datetime import datetime

from sqlalchemy import and_, cast, Date, Time
from sqlalchemy.orm import Session
from src.models import Order, OrderService, OrderStatusEnum, ScheduleSlot
from src.schemas.order_schemas import OrderRequest

def create_order(db: Session, order_data: OrderRequest):
    db_order = Order(
        office_id=order_data.office_id,
        client_id=order_data.client_id,
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