from fastapi import HTTPException
from random import randint
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src.models import Patient
from src.utils.security import create_access_token, verify_password
from src.repositories.patients import get_patient_by_email
from src.utils.jwt import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def send_verification_code(email: str):
    verification_code = randint(100000, 999999)
    return verification_code

def verify_signup(db: Session, signup_data, verification_code):
    if verification_code == signup_data.emailVerificationCode:
        hashed_password = pwd_context.hash(signup_data.password)
        patient = Patient(
            name=signup_data.name,
            surname=signup_data.surname,
            email=signup_data.email,
            phone=signup_data.phone,
            iin=signup_data.iin,
            date_of_birth=signup_data.date_of_birth,
            password=hashed_password
        )
        db.add(patient)
        db.commit()
        db.refresh(patient)

        return {"message": "Patient registered successfully", "patient_id": patient.id}
    raise HTTPException(status_code=400, detail="Invalid verification code")

def authenticate_patient(db: Session, patient):
    
    db_patient = get_patient_by_email(db, patient.email)
    if not db_patient:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(patient.password, db_patient.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_patient.id}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}