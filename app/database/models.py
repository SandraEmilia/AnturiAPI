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

