from pydantic import BaseModel
from typing import List, Literal


class OrderServiceRequest(BaseModel):
    service_name: str


class OrderRequest(BaseModel):
    office_id: int
    client_id: int
    office_name: str
    office_desc: str
    address: str
    max_capacity: int
    duration: str
    status: Literal["Booked", "Completed", "Cancelled", "Pending"]
    total_sum: float
    services: List[OrderServiceRequest]


class OrderServiceResponse(BaseModel):
    id: int
    service_name: str


class OrderResponse(BaseModel):
    id: int
    office_id: int
    client_id: int
    office_name: str
    office_desc: str
    address: str
    max_capacity: int
    duration: str
    status: str
    total_sum: float
    services: List[OrderServiceResponse]

    class Config:
        orm_mode = True

class OrderStatusRequest(BaseModel):
    id: int
    status: str