from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.repositories import order
from src.schemas.order_schemas import OrderRequest

def create_order_service(db: Session, order_data: OrderRequest):
    existing_orders = order.check_office_availability(db, order_data.office_id, order_data.duration)

    if existing_orders >= 3:
        raise HTTPException(status_code=406, detail='The office is not available for the requested duration. Maximum of 3 overlapping orders allowed.')

    return order.create_order(db, order_data)
