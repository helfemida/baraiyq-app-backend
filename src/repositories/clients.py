from sqlalchemy.orm import Session
from src.models import Client


def get_client_by_email(db: Session, email: str):
    return db.query(Client).filter(Client.email == email).first()


def get_client_by_phone(db: Session, phone: str):
    return db.query(Client).filter(Client.phone == phone).first()
