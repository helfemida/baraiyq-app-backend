# src/routing/office.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.office_schemas import OfficeResponse
from src.services.office_service import get_available_offices

router = APIRouter()

@router.get("/offices/", response_model=list[OfficeResponse])
def read_offices(db: Session = Depends(get_db)):
    offices = get_available_offices(db)
    return offices
