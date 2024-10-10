from sqlalchemy.orm import Session
from src.models import Client

def get_client_by_email(db: Session, email: str):
    return db.query(Client).filter(Client.email == email).first()

def add_client(db: Session, client: Client):
    id = db.ge