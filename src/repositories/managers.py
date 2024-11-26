from sqlalchemy.orm import Session
from src.models import Manager


def get_manager_by_email(db: Session, email: str):
    return db.query(Manager).filter(Manager.email == email).first()


def get_manager_by_phone(db: Session, phone: str):
    return db.query(Manager).filter(Manager.phone == phone).first()


def get_manager_by_id(db: Session, id: int):
    return db.query(Manager).filter(Manager.id == id).first()

