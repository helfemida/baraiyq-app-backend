from pydantic import BaseModel
from typing import List

from src.schemas.schedule_schemas import OfficeSchedule


class Feedbacks(BaseModel):
    client_id: int
    office_id: int
    title: str
    description: str
    rating: float

class OfficeFeedbacks(BaseModel):
    id: int
    fullname: str
    description: str
    rating: float

class OfficeRequest(BaseModel):
    name: str
    description: str
    address: str
    rating: float
    capacity: int
    lat: float
    lng: float

class OfficeResponse(BaseModel):
    id: int
    name: str
    description: str
    address: str
    rating: float
    capacity: int
    lat: float
    lng: float
    schedules: List[OfficeSchedule]
    feedbacks: List[OfficeFeedbacks]

    class Config:
        orm_mode = True

class OfficeInfo(BaseModel):
    id: int
    name: str
    description: str
    address: str
    rating: float
    capacity: int
    class Config:
        orm_mode = True