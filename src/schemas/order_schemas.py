from pydantic import BaseModel
from typing import List

class OrderCreate(BaseModel):
    client_id: int
    office_ids: List[int]
    total_price: float
    people_amount: int
    date: str

class OrderRequest(BaseModel):
    client_id: int
    office_id: int
    total_price: float
    people_amount: int
    date: str
    time_slots: List[int]
