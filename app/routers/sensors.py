from fastapi import APIRouter, status
from ..database import crud
from ..database.models import SensorIn, SensorOut, SensorSectionUpdate, SensorStatusUpdate, SensorWithMeasurements, SensorBySection
from typing import Optional
from datetime import datetime


router = APIRouter(prefix="/sensors", tags=["Sensors"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=SensorOut)
def add_new_sensor(sensor_in: SensorIn):
    return crud.add_new_sensor(sensor_in)

@router.patch("/{sensor_id}/status", response_model=SensorOut)
def change_status_by_sensorId(sensor_id: int, update: SensorStatusUpdate):
    return crud.change_status_by_sensorId(sensor_id, update)

@router.patch("/{sensor_id}/section", response_model=SensorOut)
def change_section_by_sensorId(sensor_id: int, update: SensorSectionUpdate):
    return crud.change_section_by_sensorId(sensor_id, update)

@router.get("", response_model=list[SensorOut])
def get_sensors(status: str | None = None):
    return crud.get_sensors(status)


@router.get("/by-section", response_model=list[SensorBySection])
def get_sensors_by_section(section: str):
    return crud.get_sensors_by_section(section)

@router.get("/{sensor_id}", response_model=SensorWithMeasurements)
def get_sensordata_by_id(
    sensor_id: int, 
    limit: int = 10, 
    start: Optional[datetime] = None, 
    end: Optional[datetime] = None):
    return crud.get_sensordata_by_id(sensor_id, limit, start, end)