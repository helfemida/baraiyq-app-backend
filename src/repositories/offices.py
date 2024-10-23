from typing import List, Type

from sqlalchemy.orm import Session
from src.models import Office, ScheduleSlot, Feedback, Client
from src.schemas.office_schemas import OfficeFeedbacks, OfficeSchedule, OfficeResponse, OfficeInfo


def get_all_offices(db: Session):
    return db.query(Office).all()

def get_office_schedules(db: Session, id: int):
    schedules = db.query(ScheduleSlot).join(Office).filter(Office.id == id).all()
    list = []

    for schedule in schedules:
        list.append({
            "id": schedule.id,
            "day": schedule.day,
            "start_time": schedule.start_time,
            "end_time": schedule.end_time,
            "booked": schedule.is_booked,
        })

    return list

def get_office_feedbacks(db: Session, id: int):
    feedbacks = db.query(Feedback).join(Client).join(Office).filter(Office.id == id).all()
    list = []

    for feedback in feedbacks:
        list.append({
            "id": feedback.id,
            "fullname": feedback.client.name + " " + feedback.client.surname,
            "title": feedback.title,
            "description": feedback.description,
            "rating": feedback.rating,
        })

    return list

def get_office_by_id(db: Session, office_id: int):
    db_office = db.query(Office).filter(Office.id == office_id).all()
    db_feedbacks = get_office_feedbacks(db, office_id)
    db_schedule = get_office_schedules(db, office_id)


    result_office = {
        "id": db_office[0].id,
        "name": db_office[0].name,
        "description": db_office[0].description,
        "address": db_office[0].address,
        "rating": db_office[0].rating,
        "schedule": db_schedule,
        "feedbacks": db_feedbacks
    }


    return result_office

