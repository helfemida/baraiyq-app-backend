from sqlalchemy.orm import Session
from src.models import Patient

def get_patient_by_email(db: Session, email: str):
    return db.query(Patient).filter(Patient.email == email).first()