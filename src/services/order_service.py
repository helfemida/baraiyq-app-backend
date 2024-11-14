from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from src.models import Order, OrderService
from src.repositories import order
from src.schemas.order_schemas import OrderRequest


def create_order_service(db: Session, order_data: OrderRequest):
    existing_orders = order.check_office_availability(db, order_data.office_id, order_data.duration)

    if existing_orders >= 3:
        raise HTTPException(status_code=406, detail='The office is not available for the requested duration. Maximum of 3 overlapping orders allowed.')
    order.book_schedule_slot(db, order_data.office_id, order_data.duration)
    return order.create_order(db, order_data)

def get_orders_by_client_id(db: Session, client_id: int):
    return db.query(Order).options(joinedload(Order.services)).filter(Order.client_id == client_id).all()

def get_order_by_id(db: Session, order_id: int):
    order = db.query(Order).options(joinedload(Order.services)).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

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
