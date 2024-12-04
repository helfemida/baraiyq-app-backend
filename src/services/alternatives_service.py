from sqlalchemy.orm import Session

from src.repositories.alternatives import submit_alternatives
from src.schemas.alternative_schemas import AlternativeRequestBase


def submit_alternatives_service(request: AlternativeRequestBase, db: Session):
    return submit_alternatives(request, db)