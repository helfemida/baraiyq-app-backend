from sqlalchemy.orm import Session
from src.models import Client


def get_client_by_email(db: Session, email: str):
    return db.query(Client).filter(Client.email == email).first()


def get_client_by_phone(db: Session, phone: str):
    return db.query(Client).filter(Client.phone == phone).first()



def get_client_by_id(db: Session, id: int):
    return db.query(Client).filter(Client.id == id).first()

