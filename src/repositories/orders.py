from sqlalchemy.orm import Session
from src.models import Order

from src.schemas.order_schemas import OrderRequest


def create_order(db: Session, order_data: OrderRequest):
    db_order = Order(
        client_id=order_data.client_id,
        office_ids=order_data.office_ids,
        total_price=order_data.total_price,
        people_amount=order_data.people_amount,
        date=order_data.date,
        start_time=order_data.start_time,
        end_time=order_data.end_time,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def check_existing_orders(db: Session, client_id: int, date: str, start_time: str, end_time: str):
    existing_orders = db.query(Order).filter(
        Order.client_id == client_id,
        Order.date == date,
        Order.start_time < end_time,
        Order.end_time > start_time
    ).all()
    return existing_orders
