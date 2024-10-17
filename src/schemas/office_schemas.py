from pydantic import BaseModel
from typing import List

# class Feedback(BaseModel):
#     fullname: str
#     title: str
#     description: str

class OfficeScheduleResponse(BaseModel):
    day: str
    start_time: str
    end_time: str
    is_booked: bool

class OfficeResponse(BaseModel):
    id: int
    name: str
    description: str
    address: str
    rating: float
    lat: float
    lng: float
    schedule: List[OfficeScheduleResponse]
    # feedbacks: List[Feedback]