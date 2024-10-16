from pydantic import BaseModel
from typing import List

# class Feedback(BaseModel):
#     fullname: str
#     title: str
#     description: str

class OfficeResponse(BaseModel):
    id: int
    name: str
    description: str
    address: str
    rating: float
    lat: float
    lng: float
    # feedbacks: List[Feedback]
