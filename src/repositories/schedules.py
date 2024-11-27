from sqlalchemy.orm import Session

from src.models import ScheduleSlot
from src.schemas.schedule_schemas import ScheduleRequest


def create_schedule(db: Session, office_id: int, schedule_data: ScheduleRequest):
    schedule = ScheduleSlot(
        office_id=office_id,
        day=schedule_data.day,
        start_time=schedule_data.start_time,
        end_time=schedule_data.end_time,
        is_booked=False,
    )
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule