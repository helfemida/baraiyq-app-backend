from sqlalchemy.orm import Session

from src.models import AlternativeRequest
from src.schemas.alternative_schemas import AlternativeRequestBase


def submit_alternatives(request: AlternativeRequestBase, db: Session):
    alternatives = AlternativeRequest(
        client_id = request.client_id,
        office_id = request.office_id,
        requested_date = request.requested_date,
        people_amount = request.people_amount
    )

    db.add(alternatives)
    db.commit()
    db.refresh(alternatives)
    return alternatives