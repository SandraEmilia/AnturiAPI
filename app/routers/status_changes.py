from fastapi import APIRouter, status
from ..database import crud
from ..database.models import StatuschangesBase, SensorStatusUpdate

router = APIRouter(prefix="/sensors", tags=["Status_changes"])

@router.get("/{sensor_id}/status_changes", response_model=list[StatuschangesBase])
def get_statuschanges_by_sensorId(sensor_id: int):
    return crud.get_statuschanges_by_sensorId(sensor_id)

