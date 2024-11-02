from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models import Order, ScheduleSlot
from src.schemas.order_schemas import OrderRequest


def create_order(db: Session, order_data: OrderRequest):
    db_order = Order(
        client_id=order_data.client_id,
        office_id=order_data.office_id,
        total_price=order_data.total_price,
        people_amount=order_data.people_amount,
        date=order_data.date
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for slot in order_data.time_slots:
        db_slot = db.query(ScheduleSlot).filter(ScheduleSlot.id == slot.slot_id).first()
        if not db_slot or db_slot.is_booked:
            raise HTTPException(status_code=400, detail=f"Slot ID {slot.slot_id} is not available.")

        db_slot.order_id = db_order.id
        db_slot.is_booked = True

    db.commit()
    return db_order


def check_existing_orders(db: Session, client_id: int, date: str):
    existing_orders = db.query(Order).filter(
        Order.client_id == client_id,
        Order.date == date
    ).all()
    return existing_orders
