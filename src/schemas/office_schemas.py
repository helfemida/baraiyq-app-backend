from pydantic import BaseModel
from typing import List

class OfficeFeedbacks(BaseModel):
    id: int
    fullname: str
    description: str
    rating: float


class OfficeSchedule(BaseModel):
    id: int
    day: str
    start_time: str
    end_time: str
    is_booked: bool
    class Config:
        orm_mode = True

class OfficeResponse(BaseModel):
    id: int
    name: str
    description: str
    address: str
    rating: float
    capacity: int
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