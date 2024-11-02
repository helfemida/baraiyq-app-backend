from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.repositories.orders import create_order, check_existing_orders
from src.schemas.order_schemas import OrderRequest

def book_offices(db: Session, order_request: OrderRequest):
    existing_orders = check_existing_orders(
        db=db,
        client_id=order_request.client_id,
        date=order_request.date
    )

    if len(existing_orders) >= 3:
        raise HTTPException(status_code=406, detail="You cannot book more than 3 orders for the same date.")

    new_order = create_order(db=db, order_data=order_request)
    return new_order
