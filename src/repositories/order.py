from datetime import datetime

from sqlalchemy import and_
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

    active_orders = db.query(Order).filter(
        and_(
            Order.office_id == office_id,
            Order.status == OrderStatusEnum.Booked
        )
    ).all()

    overlapping_orders = sum(
        1 for order in active_orders
        if (
                parse_func(order.duration)[0] < end_datetime and
                parse_func(order.duration)[1] > start_datetime
        )
    )

    return overlapping_orders
