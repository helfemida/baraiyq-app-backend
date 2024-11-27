from pydantic import BaseModel


class OfficeSchedule(BaseModel):
    id: int
    day: str
    start_time: str
    end_time: str
    is_booked: bool
    class Config:
        orm_mode = True

class ScheduleRequest(BaseModel):
    day: str
    start_time: str
    end_time: str