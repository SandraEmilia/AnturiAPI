from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List


class SensorBase(SQLModel):
    name: str
    section: str
    status: str

class SensorIn(SensorBase):
    pass

class SensorOut(SensorBase, table=True):
    __tablename__ = "sensor"
    id: int | None = Field(default=None, primary_key=True)

class MeasurementBase(SQLModel):
    temperature: float
    timestamp: datetime

class MeasurementIn(SQLModel):
    sensor_id: int
    temperature: float
    timestamp: datetime | None = None
    
class Measurement(MeasurementBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sensor_id: int = Field(foreign_key="sensor.id")

class MeasurementOut(MeasurementBase):
    id: int
    sensor_id: int

class StatuschangesBase(SQLModel):
    old_status: str
    new_status: str
    timestamp: datetime

class StatusChange(StatuschangesBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sensor_id: int = Field(foreign_key="sensor.id")

class SensorWithMeasurements(SensorBase):
    id: int
    measurements: list[MeasurementOut]

class SensorStatusUpdate(SQLModel):
    status: str

class SensorSectionUpdate(SQLModel):
    section: str

class ErrorEvent(SQLModel):
    sensor_id : int
    timestamp: datetime

class SensorBySection(SQLModel):
    id: int
    section: str
    status: str
    last_temperature: float | None
    last_timestamp: datetime | None
    