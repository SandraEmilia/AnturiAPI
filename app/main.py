from fastapi import FastAPI, HTTPException, Response, status
from typing import Optional
from datetime import datetime
from .database.models import SensorIn, SensorOut, SensorWithMeasurements, SensorStatusUpdate, SensorSectionUpdate, ErrorEvent

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

@app.patch("/sensors/{sensor_id}/status")
def change_status_by_sensorId(sensor_id: int, update: SensorStatusUpdate):
    sensor = next((s for s in sensors if s["id"] == sensor_id), None)
    if sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'sensor with id {sensor_id} not found.'
        )
    old_status = sensor["status"]
    new_status = update.status

    sensor["status"] = new_status

    status_changes.append(
        {
            "id": len(status_changes) +1,
            "sensor_id": sensor_id,
            "old_status": old_status,
            "new_status": new_status,
            "timestamp": datetime.now(),
        }
    )
    return sensor

@app.patch("/sensors/{sensor_id}/section")
def change_section_by_sensorId(sensor_id: int, update: SensorSectionUpdate):
    sensor = next((s for s in sensors if s["id"] == sensor_id), None)
    if sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'sensor with id {sensor_id} not found.'
        )
    new_section = update.section
    sensor["section"] = new_section

    return sensor


@app.get("/sensors")
def get_sensors(status: str | None = None):
    if status:
        filtered = [s for s in sensors if s["status"] == status]
        if not filtered:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_fOUND,
                detail=f'No sensors found with status "{status}"'
            )
        return filtered
    return sensors

@app.get("/sensors/by-section")
def get_sensors_by_section(section: str):

    filtered = [s for s in sensors if s["section"] == section]

    result = []

    for s in filtered:
        last_measurement = max(
            (m for m in measurements if m["sensor_id"] == s["id"]),
            key=lambda m: m["timestamp"],
            default=None
        )
        result.append({
            "id": s["id"],
            "section": s["section"],
            "status": s["status"],
            "last_temperature": last_measurement["temperature"] if last_measurement else None,
            "last_timestamp": last_measurement["timestamp"] if last_measurement else None,
        })
    return result

@app.get("/sensors/{sensor_id}", response_model=SensorWithMeasurements)
def get_sensordata_by_id(
    sensor_id: int, 
    limit: int = 10, 
    start: Optional[datetime] = None, 
    end: Optional[datetime] = None):
    
    sensor = next((s for s in sensors if s ["id"] == sensor_id), None)
    if sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'sensor with id {sensor_id} not found.'
        )
    
    sensor_measurements = [
        m for m in measurements if m["sensor_id"] == sensor_id
    ]
    
    if start is not None and end is not None:
        sensor_measurements = [
            m for m in sensor_measurements if start <= m["timestamp"] <= end
        ]
    else:
        #Muuten uusimmat "limit" mittausta
        sensor_measurements = sorted(
            sensor_measurements,
            key=lambda m: m["timestamp"],
            reverse=True
        )[:limit]

    return SensorWithMeasurements(
        **sensor,
        measurements=sensor_measurements,
    )


@app.get("/sensors/{sensor_id}/status_changes")
def get_statuschanges_by_sensorId(sensor_id: int):
    sensor = next((s for s in sensors if s["id"] == sensor_id), None)
    if sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'sensor with id {sensor_id} not found.'
        )
    changes = [
        c for c in status_changes if c["sensor_id"] == sensor_id
    ]
    return changes


@app.get("/stats/error-events", response_model=list[ErrorEvent])
def get_error_events(sensor_id: int | None = None):

    events = [
        c for c in status_changes if c["new_status"] == "error"
    ]

    if sensor_id is not None:
        events = [c for c in events if c["sensor_id"] == sensor_id]

    return [
        ErrorEvent(sensor_id=e["sensor_id"],timestamp=e["timestamp"])
        for e in events
    ]


@app.delete("/measurements/{measurement_id}")
def delete_measurement_by_id(measurement_id: int):
    measurement_index = -1
    for i, m in enumerate(measurements):
        if m["id"] == measurement_id:
            measurement_index = i
            break
    if measurement_index == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'measurement with id {measurement_id} not found.'
        )
    del measurements[measurement_index]
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) 
    