from fastapi import APIRouter, status, Depends
from sqlmodel import Session
from datetime import datetime

from ..database import crud
from ..database.models import( 
    SensorIn, 
    SensorOut, 
    SensorSectionUpdate, 
    SensorStatusUpdate, 
    SensorWithMeasurements, 
    SensorBySection,
)
from ..database.database import get_session


router = APIRouter(prefix="/sensors", tags=["Sensors"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=SensorOut)
def add_new_sensor(*, session: Session = Depends(get_session), sensor_in: SensorIn):
    return crud.add_new_sensor(session, sensor_in)

@router.patch("/{sensor_id}/status", response_model=SensorOut)
def change_status_by_sensorId(*, session: Session = Depends(get_session), sensor_id: int, update: SensorStatusUpdate):
    return crud.change_status_by_sensorId(session, sensor_id, update)

@router.patch("/{sensor_id}/section", response_model=SensorOut)
def change_section_by_sensorId(*, session: Session = Depends(get_session), sensor_id: int, update: SensorSectionUpdate):
    return crud.change_section_by_sensorId(session, sensor_id, update)

@router.get("", response_model=list[SensorOut])
def get_sensors(*, session: Session = Depends(get_session), status: str | None = None):
    return crud.get_sensors(session, status)


@router.get("/by-section", response_model=list[SensorBySection])
def get_sensors_by_section(*, session: Session = Depends(get_session), section: str):
    return crud.get_sensors_by_section(session, section)

@router.get("/{sensor_id}", response_model=SensorWithMeasurements)
def get_sensordata_by_id(
    sensor_id: int, 
    limit: int = 10, 
    start: datetime | None = None, 
    end: datetime | None  = None,
    session: Session = Depends(get_session),
):
    return crud.get_sensordata_by_id(session, sensor_id, limit, start, end)