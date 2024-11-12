from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from src.models import Order
from src.repositories import order
from src.schemas.order_schemas import OrderRequest, OrderResponse


def create_order_service(db: Session, order_data: OrderRequest):
    existing_orders = order.check_office_availability(db, order_data.office_id, order_data.duration)

    if existing_orders >= 3:
        raise HTTPException(status_code=406, detail='The office is not available for the requested duration. Maximum of 3 overlapping orders allowed.')

    return order.create_order(db, order_data)

def get_orders_by_client_id(db: Session, client_id: int):
    return db.query(Order).options(joinedload(Order.services)).filter(Order.client_id == client_id).all()

def get_order_by_id(db: Session, order_id: int):
    order = db.query(Order).options(joinedload(Order.services)).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
