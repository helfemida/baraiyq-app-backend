from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.utils.jwt import SECRET_KEY, ALGORITHM
from src.repositories.clients import get_client_by_id

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(db: Session, user_id: int, expires_delta: timedelta = None):
    # to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode = ({"exp": expire})

    user_info = get_client_by_id(db, user_id)

    to_encode.update(
        {"id": user_info.id,
         "name": user_info.name,
         "surname": user_info.surname,
         "email": user_info.email,
         "phone": user_info.phone,
         "date_of_birth": str(user_info.date_of_birth)})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
