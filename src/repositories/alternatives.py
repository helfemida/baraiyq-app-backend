from datetime import datetime

from sqlalchemy.orm import Session

from src.models import AlternativeRequest, AlternativeResponse
from src.repositories.clients import get_client_by_id
from src.repositories.offices import get_office_by_id
from src.schemas.alternative_schemas import AlternativeRequestBase, AlternativeResponseBase, AlternativeFilterRequest


def submit_alternatives(request: AlternativeRequestBase, db: Session):
    alternatives = AlternativeRequest(
        client_id=request.client_id,
        office_id=request.office_id,
        requested_date=request.requested_date,
        people_amount=request.people_amount
    )

    db.add(alternatives)
    db.commit()
    db.refresh(alternatives)
    return alternatives


def get_all_requests(db: Session):
    return db.query(AlternativeRequest).all()


def get_all_requests_by_filter(request: AlternativeFilterRequest, db: Session):
    # Создаем базовый запрос
    query = db.query(AlternativeRequest)

    # Добавляем фильтр по датам
    if request.startDate and request.endDate:
        query = query.filter(
            AlternativeRequest.requested_date >= request.startDate,
            AlternativeRequest.requested_date <= request.endDate
        )
    elif request.startDate is None and request.endDate is None:
        pass  # Ничего не добавляем, если обе даты None
    else:
        raise ValueError("startDate и endDate должны быть либо оба заполнены, либо оба пусты")

    # Добавляем фильтр по количеству людей
    if request.amountStart is not None and request.amountEnd is not None:
        query = query.filter(
            AlternativeRequest.people_amount >= request.amountStart,
            AlternativeRequest.people_amount <= request.amountEnd
        )
    elif request.amountStart is None and request.amountEnd is None:
        pass  # Ничего не добавляем, если оба значения None
    else:
        raise ValueError("amountStart и amountEnd должны быть либо оба заполнены, либо оба пусты")

    # Добавляем фильтр по clientIds
    if request.clientIds:
        query = query.filter(AlternativeRequest.client_id.in_(request.clientIds))

    # Добавляем фильтр по officeIds
    if request.officeIds:
        query = query.filter(AlternativeRequest.office_id.in_(request.officeIds))

    return query.all()


def get_request_by_id(db: Session, request_id: int):
    return db.query(AlternativeRequest).filter(AlternativeRequest.id == request_id).first()


def add_response(db: Session, request: AlternativeResponseBase):
    response = AlternativeResponse(
        request_id=request.request_id,
        manager_id=request.manager_id,
        response_details=request.response_details
    )

    db.add(response)
    db.commit()
    db.refresh(response)
    return response


def toJsonSerializable(db_alt: list[AlternativeRequestBase], db: Session):
    all_alternatives = []

    for alt in db_alt:
        db_client = get_client_by_id(db, alt.client_id)
        db_office = get_office_by_id(db, alt.office_id)

        created_at_str = alt.created_at.isoformat() if isinstance(alt.created_at, datetime) else str(
            alt.created_at)

        alt_dict = {
            "id": alt.id,
            "client_id": db_client.id,
            "client_name": db_client.name,
            "client_surname": db_client.surname,
            "client_phone": db_client.phone,
            "client_email": db_client.email,
            "office_id": db_office.get("id"),
            "office_name": db_office.get("name"),
            "office_desc": db_office.get("description"),
            "address": db_office.get("address"),
            "max_capacity": db_office.get("capacity"),
            "requested_date": alt.requested_date,
            "people_amount": alt.people_amount,
            "created_at": created_at_str
        }
        all_alternatives.append(alt_dict)

    return all_alternatives
