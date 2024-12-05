from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models import Office, ScheduleSlot, Feedback, Client
from src.schemas.office_schemas import Feedbacks, OfficeFeedbacks, OfficeResponse, OfficeRequest, OfficeUpdateRequest
from src.schemas.schedule_schemas import OfficeSchedule


def get_all_offices(db: Session):
    return db.query(Office).all()


def get_office_schedules_dto(db: Session, id: int):
    return db.query(ScheduleSlot).join(Office).filter(Office.id == id).all()


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


def get_office_dto_by_id(db: Session, office_id: int):
    db_office = db.query(Office).filter(Office.id == office_id).all()
    db_feedbacks = get_office_feedbacks(db, office_id)
    feedback_dto = []

    for db_feedback in db_feedbacks:
        feedback = OfficeFeedbacks(
            id=db_feedback.id,
            fullname=db_feedback.client.name + " " + feedback.client.surname,
            description=db_feedback.description,
            rating=db_feedback.rating,
        )
        feedback_dto.append(feedback)

    db_schedules = get_office_schedules_dto(db, office_id)
    all_schedules = []

    for db_schedule in db_schedules:
        schedule = OfficeSchedule(
            id=db_schedule.id,
            day=db_schedule.day,
            start_time=db_schedule.start_time,
            end_time=db_schedule.end_time,
            is_booked=db_schedule.is_booked
        )
        all_schedules.append(schedule)

    result_office = OfficeResponse(
        id=db_office[0].id,
        name=db_office[0].name,
        description=db_office[0].description,
        address=db_office[0].address,
        rating=db_office[0].rating,
        capacity=db_office[0].capacity,
        lat=db_office[0].lat,
        lng=db_office[0].lng,
        schedules=all_schedules,
        feedbacks=feedback_dto
    )

    return result_office


def get_office_by_id(db: Session, office_id: int):
    db_office = db.query(Office).filter(Office.id == office_id).first()

    if db_office is None:
        raise HTTPException(status_code=404, detail="Office not found")

    db_feedbacks = get_office_feedbacks(db, office_id)
    db_schedule = get_office_schedules(db, office_id)

    result_office = {
        "id": db_office.id,
        "name": db_office.name,
        "description": db_office.description,
        "address": db_office.address,
        "rating": db_office.rating,
        "capacity": db_office.capacity,
        "lat": db_office.lat,
        "lng": db_office.lng,
        "schedule": db_schedule,
        "feedbacks": db_feedbacks
    }

    return result_office


def add_feedback(db: Session, feedback_data: Feedbacks):
    feedback = Feedback(
        client_id=feedback_data.client_id,
        office_id=feedback_data.office_id,
        title=feedback_data.title,
        description=feedback_data.description,
        rating=feedback_data.rating
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return {
        "id": feedback.id,
        "client_id": feedback.client_id,
        "office_id": feedback.office_id,
        "title": feedback.title,
        "description": feedback.description,
        "rating": feedback.rating
    }


def get_office_by_name(db: Session, office_name: str):
    return db.query(Office).filter(Office.name.ilike(f"%{office_name}%")).all()


def create_office_manager(db: Session, request: OfficeRequest):
    office = Office(
        name=request.name,
        description=request.description,
        address=request.address,
        rating=request.rating,
        capacity=request.capacity,
        lat=request.lat,
        lng=request.lng
    )
    db.add(office)
    db.commit()
    db.refresh(office)
    return office


def update_office(db: Session, request: OfficeUpdateRequest):
    office = db.query(Office).filter(Office.id == request.id).first()

    if request.name is not None:
        office.name = request.name
    if request.description is not None:
        office.description = request.description
    if request.address is not None:
        office.address = request.address
    if request.rating is not None:
        office.rating = request.rating
    if request.capacity is not None:
        office.capacity = request.capacity
    if request.lat is not None:
        office.lat = request.lat
    if request.lng is not None:
        office.lng = request.lng

    db.commit()
    db.refresh(office)

    return office


def delete_office(db: Session, office_id: int):
    office = db.query(Office).filter(Office.id == office_id).first()
    db.query(ScheduleSlot).filter(ScheduleSlot.office_id == office_id).delete()
    db.query(Feedback).filter(Feedback.office_id == office_id).delete()

    db.delete(office)
    db.commit()

    return True
