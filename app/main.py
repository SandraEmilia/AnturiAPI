from fastapi import FastAPI, HTTPException, Response, status
from datetime import datetime
from .database.models import SensorIn, SensorOut

app = FastAPI()

sensors = [
    {"id": 1, "name": "Sensor1", "section": "A1", "status": "online"},
    {"id": 2, "name": "Sensor2", "section": "A2", "status": "offline"},
    {"id": 3, "name": "Sensor3", "section": "B1", "status": "online"},
    {"id": 4, "name": "Sensor4", "section": "C3", "status": "online"},
]

measurements = [
    {"id": 1, "sensor_id": 1, "temperature": 21.5, "timestamp": datetime(2025, 11, 26, 10, 0, 0)},
    {"id": 2, "sensor_id": 2, "temperature": 20.6, "timestamp": datetime(2025, 11, 26, 11, 30, 5)},
    {"id": 3, "sensor_id": 2, "temperature": 20.7, "timestamp": datetime(2025, 11, 26, 11, 31, 0)},
    {"id": 4, "sensor_id": 3, "temperature": 21.2, "timestamp": datetime(2025, 11, 26, 12, 1, 0)},
]

status_changes = [
    {"id": 1, "sensor_id": 1, "old_status": "online", "new_status": "offline", "timestamp": datetime(2025, 11, 26, 10, 45, 0 )},
]



@app.post("/sensors")
def add_new_sensor(sensor_in : SensorIn):
    new_id = sensors[-1]["id"]+1
    sensor = SensorOut(id=new_id, **sensor_in.model_dump())
    sensors.append(sensor.model_dump())
    return sensor


@app.get("/sensors")
def get_all_sensors():
    return sensors

