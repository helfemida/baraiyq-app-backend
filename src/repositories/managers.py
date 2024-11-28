from sqlalchemy.orm import Session
from src.models import Manager, Order


def get_manager_by_email(db: Session, email: str):
    return db.query(Manager).filter(Manager.email == email).first()


def get_manager_by_phone(db: Session, phone: str):
    return db.query(Manager).filter(Manager.phone == phone).first()


def get_admin_privelegy_by_manager_id(db: Session, manager_id: int) -> bool:
    return db.query(Manager.admin_privelegy).filter(Manager.id == manager_id).first()


def get_manager_by_id(db: Session, id: int):
    return db.query(Manager).filter(Manager.id == id).first()


def get_last_assigned_manager(db: Session):
    last_order = db.query(Order).order_by(Order.id.desc()).first()
    return last_order.manager_id


def assign_manager(last_manager_id: int):
    MANAGER_IDS = [1, 4, 5]
    current_index = MANAGER_IDS.index(last_manager_id)
    next_index = (current_index + 1) % len(MANAGER_IDS)
    return MANAGER_IDS[next_index]
