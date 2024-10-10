from pydantic import BaseModel, EmailStr
from datetime import date


class SignUpRequest(BaseModel):
    name: str
    surname: str
    email: str
    phone: str
    date_of_birth: str
    password: str



    
