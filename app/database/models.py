from pydantic import BaseModel
from datetime import datetime

class SensorBase(BaseModel):
    name: str
    section: str
    status: str

class SensorIn(SensorBase):
    pass

class SensorOut(SensorBase):
    id: int

class MeasurementBase(BaseModel):
    id: int
    sensor_id: int
    temperature: float
    timestamp: datetime

class StatuschangesBase(BaseModel):
    id: int
    sensor_id: int
    old_status: str
    new_status: str
    timestamp: datetime

class SensorWithMeasurements(SensorBase):
    measurements: list[MeasurementBase]
