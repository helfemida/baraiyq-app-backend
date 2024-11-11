from sqlalchemy.orm import Session
from src.repositories import order
from src.schemas.order_schemas import OrderRequest

def create_order_service(db: Session, order_data: OrderRequest):
    return order.create_order(db, order_data)
