from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.repositories.offices import get_all_offices, get_office_by_id, add_feedback, get_office_by_name
from src.schemas.office_schemas import Feedbacks


def get_offices_info(db: Session):
    db_offices = get_all_offices(db=db)

    if not db_offices:
        raise HTTPException(status_code=404, detail="no offices available")

    offices_info = []

    for office in db_offices:
        office_dict = {
            "id": office.id,
            "name": office.name,
            "description": office.description,
            "address": office.address,
            "rating": office.rating,
            "capacity": office.capacity
        }
        offices_info.append(office_dict)

    return offices_info

def get_single_office(id: int, db: Session):
    return get_office_by_id(db, id)

def create_feedback(db: Session, feedback_data: Feedbacks):
    feedback_dict = add_feedback(db, feedback_data)
    return feedback_dict

def search_offices_service(db: Session, office_name: str):
    return get_office_by_name(db, office_name)
