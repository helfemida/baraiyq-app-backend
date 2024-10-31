from pydantic import BaseModel
from typing import List

class OrderRequest(BaseModel):
    client_id: int
    office_ids: List[int]
    total_price: float
    people_amount: int
    date: str
    start_time: str
    end_time: str

class OrderResponse(BaseModel):
    id: int
    client_id: int
    office_ids: List[int]
    total_price: float
    people_amount: int
    date: str
    start_time: str
    end_time: str

    class Config:
        orm_mode = True
