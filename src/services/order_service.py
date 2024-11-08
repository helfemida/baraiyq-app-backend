from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models import Order, ScheduleSlot
from src.schemas.order_schemas import OrderRequest


def create_order(db: Session, order_data: OrderRequest):
    office_orders = db.query(Order).filter(Order.office_id == order_data.office_id,
                                           Order.date == order_data.date).all()
    if len(office_orders) >= 3:
        raise HTTPException(status_code=406, detail="This office is already booked for 3 orders on this date")

    slots = db.query(ScheduleSlot).filter(ScheduleSlot.id.in_(order_data.time_slots),
                                          ScheduleSlot.is_booked == False).all()

    if len(slots) != len(order_data.time_slots):
        raise HTTPException(status_code=406, detail="One or more time slots are already booked")

    for slot in slots:
        slot.is_booked = True

    new_order = Order(
        client_id=order_data.client_id,
        office_id=order_data.office_id,
        total_price=order_data.total_price,
        people_amount=order_data.people_amount,
        date=order_data.date,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    db.bulk_save_objects(slots)
    db.commit()

    return {
        "id": new_order.id,
        "client_id": new_order.client_id,
        "office_id": new_order.office_id,
        "total_price": new_order.total_price,
        "people_amount": new_order.people_amount,
        "date": new_order.date,
        "booked_slots": order_data.time_slots
    }