from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..database import crud
from ..database.models import StatuschangesBase

from ..database.database import get_session

router = APIRouter(prefix="/sensors", tags=["Status_changes"])

@router.get("/{sensor_id}/status_changes", response_model=list[StatuschangesBase])
def get_statuschanges_by_sensorId(*, session: Session = Depends(get_session), sensor_id: int):
    return crud.get_statuschanges_by_sensorId(session, sensor_id)

