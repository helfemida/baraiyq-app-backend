from pydantic import BaseModel, EmailStr
from datetime import date

class VerificationRequest(BaseModel):
    email: EmailStr

class SignUpRequest(BaseModel):
    name: str
    surname: str
    email: EmailStr
    phone: str
    iin: int
    date_of_birth: str
    emailVerificationCode: int
    password: str

class SignInRequest(BaseModel):
    email: EmailStr 
    phone: str | None
    password: str

    
