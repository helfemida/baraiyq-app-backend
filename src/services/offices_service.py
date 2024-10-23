from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.repositories.offices import get_all_offices, get_office_by_id
from src.schemas.office_schemas import OfficeInfo


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


