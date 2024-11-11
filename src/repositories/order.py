from datetime import datetime

from sqlalchemy.orm import Session
from src.models import Order, OrderService, OrderStatusEnum
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
