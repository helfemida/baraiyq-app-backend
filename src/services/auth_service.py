from fastapi import HTTPException
from random import randint
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src.models import Client
from src.schemas.auth_schemas import SignUpRequest
from src.utils.security import create_access_token, verify_password
from src.repositories.clients import get_client_by_email, get_client_by_phone
from src.utils.jwt import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_signup(db: Session, signup_data: SignUpRequest):
    print(signup_data.name)
    print(signup_data.surname)
    print(signup_data.email)
    print(signup_data.phone)
    print(signup_data.password)
    print(signup_data.date_of_birth)

    existing_client_by_email = get_client_by_email(db, email=signup_data.email)
    if existing_client_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_client_by_phone = get_client_by_phone(db, phone=signup_data.phone)
    if existing_client_by_phone:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    hashed_password = pwd_context.hash(signup_data.password)

    client = Client(
        name=signup_data.name,
        surname=signup_data.surname,
        email=signup_data.email,
        phone=signup_data.phone,

        date_of_birth=signup_data.date_of_birth,
        password=hashed_password
    )

    print(client)
    db.add(client)
    db.commit()
    db.refresh(client)

    return {"message": "Client registered successfully", "client_id": client.id}


def authenticate_client(db: Session, email: str, password: str):
    db_client = get_client_by_email(db, email)
    if not db_client:
        raise HTTPException(status_code=400, detail="no such email.")

    if not verify_password(password, db_client.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_client.id}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


def authenticate_client_phone(db: Session, phone: str, password: str):
    db_client = get_client_by_phone(db, phone)
    if not db_client:
        raise HTTPException(status_code=400, detail="no such phone.")

    if not verify_password(password, db_client.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_client.id}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
