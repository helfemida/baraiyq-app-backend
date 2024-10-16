from pydantic import BaseModel, EmailStr



class SignUpRequest(BaseModel):
    name: str
    surname: str
    email: str
    phone: str
    date_of_birth: str
    password: str


class SignInEmailRequest(BaseModel):
    email: str
    password: str


class SignInPhoneRequest(BaseModel):
    phone: str
    password: str



