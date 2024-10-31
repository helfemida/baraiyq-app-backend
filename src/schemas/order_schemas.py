from pydantic import BaseModel
from typing import List

class TimeSlot(BaseModel):
    office_id: int
    start_time: str
    end_time: str

class OrderRequest(BaseModel):
    client_id: int
    office_ids: List[int]
    total_price: float
    people_amount: int
    date: str
    time_slots: List[TimeSlot]

class OrderResponse(BaseModel):
    id: int
    client_id: int
    office_ids: List[int]
    total_price: float
    people_amount: int
    date: str
    time_slots: List[TimeSlot]

    class Config:
        orm_mode = True
