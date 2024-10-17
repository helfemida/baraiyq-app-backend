from typing import List, Dict, Any
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from src.database import get_db
from src.models import Office
from src.schemas.office_schemas import OfficeResponse, OfficeScheduleResponse

def get_available_offices(office_id: int, db: Session = Depends(get_db)):
    office = db.query(Office).filter(Office.id == office_id).first()

    if not office:
        raise NoResultFound(f"Office with ID {office_id} not found")

    office_schedule = [
        OfficeScheduleResponse(
            day=schedule.day,
            start_time=schedule.start_time,
            end_time=schedule.end_time,
            is_booked=schedule.is_booked
        )
        for schedule in office.schedule
    ]

    return OfficeResponse(
        id=office.id,
        name=office.name,
        description=office.description,
        address=office.address,
        rating=office.rating,
        lat=office.lat,
        lng=office.lng,
        schedule=office_schedule
    )