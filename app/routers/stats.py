from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..database import crud
from ..database.models import ErrorEvent

from ..database.database import get_session


router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get("/error-events", response_model=list[ErrorEvent])
def get_error_events(*, session: Session = Depends(get_session), sensor_id: int | None = None):
    return crud.get_error_events(session, sensor_id)
