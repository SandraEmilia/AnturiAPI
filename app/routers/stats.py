from fastapi import APIRouter, status
from ..database import crud
from ..database.models import ErrorEvent

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get("/error-events", response_model=list[ErrorEvent])
def get_error_events(sensor_id: int | None = None):
    return crud.get_error_events(sensor_id)
