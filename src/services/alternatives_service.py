from sqlalchemy.orm import Session

from src.repositories.alternatives import submit_alternatives, get_all_requests, toJsonSerializable, get_request_by_id, \
    add_response
from src.schemas.alternative_schemas import AlternativeRequestBase, AlternativeResponseBase


def submit_alternatives_service(request: AlternativeRequestBase, db: Session):
    return submit_alternatives(request, db)

def get_all_alternatives_service(db: Session):
    return toJsonSerializable(get_all_requests(db), db)

def add_response_service(response: AlternativeResponseBase, db: Session):
    return add_response(db, response)
