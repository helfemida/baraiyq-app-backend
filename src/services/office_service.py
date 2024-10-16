from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Office

def get_available_offices(db: Session = Depends(get_db())):
    return db.query(Office).all()
