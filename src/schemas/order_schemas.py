from pydantic import BaseModel
from typing import List

class OrderRequest(BaseModel):
    client_id: int
    office_id: int
    total_price: float
    people_amount: int
    date: str
    time_slots: List[int]

class OrderResponse(BaseModel):
    id: int
    client_id: int
    office_id: int
    total_price: float
    people_amount: int
    date: str
    time_slots: List[int]

    class Config:
        orm_mode = True
