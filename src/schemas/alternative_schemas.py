from pydantic import BaseModel

class AlternativeRequestBase(BaseModel):
    client_id: int
    office_id: int
    requested_date: str
    people_amount: int

class AlternativeResponseBase(BaseModel):
    request_id: int
    manager_id: int
    response_details: str

class AlternativeResponseResponse(AlternativeResponseBase):
    id: int
    created_at: str

    class Config:
        orm_mode = True