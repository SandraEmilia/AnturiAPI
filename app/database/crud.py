from datetime import datetime
from typing import Optional, List
from fastapi import HTTPException, status
from sqlmodel import Session, select

from .models import (
    SensorIn,
    SensorOut,
    SensorStatusUpdate,
    SensorSectionUpdate,
    SensorWithMeasurements,
    Measurement,
    MeasurementIn,
    MeasurementOut,
    StatusChange,
    ErrorEvent,
    SensorBySection,
)

#SENSORIT

def add_new_sensor(session: Session, sensor_in : SensorIn) -> SensorOut:
    sensor = SensorOut(**sensor_in.model_dump())
    session.add(sensor)
    session.commit()
    session.refresh(sensor)
    return sensor

def change_status_by_sensorId(
    session: Session, sensor_id: int, update: SensorStatusUpdate) -> SensorOut:
    sensor = session.get(SensorOut, sensor_id)
    if sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'sensor with id {sensor_id} not found.'
        )
    
    old_status = sensor.status
    new_status = update.status

    sensor.status = new_status

    status_change = StatusChange(

            sensor_id=sensor_id,
            old_status=old_status,
            new_status=new_status,
            timestamp=datetime.now(),
    
    )

    session.add(sensor)
    session.add(status_change)
    session.commit()
    session.refresh(sensor)

    return sensor


def change_section_by_sensorId(
    session: Session, sensor_id: int, update: SensorSectionUpdate) -> SensorOut:
    sensor = session.get(SensorOut, sensor_id)
    if sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'sensor with id {sensor_id} not found.'
        )
    
    sensor.section = update.section
    session.add(sensor)
    session.commit()
    session.refresh(sensor)


    return sensor

def get_sensors(
    session: Session, status_filter: Optional[str] = None) -> SensorOut:
    query = select(SensorOut)
    
    if status_filter is not None:
        query = query.where(SensorOut.status == status_filter)
        
    sensors = session.exec(query).all()

    if status_filter is not None and not sensors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No sensors found with status "{status}"'
        )
        
        
    return sensors

def get_sensordata_by_id(
    session: Session,
    sensor_id: int, 
    limit: int = 10, 
    start: Optional[datetime] = None, 
    end: Optional[datetime] = None,
) -> SensorWithMeasurements:
    
    sensor = session.get(SensorOut, sensor_id)
    if sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'sensor with id {sensor_id} not found.'
        )
    query = select(Measurement).where(Measurement.sensor_id == sensor_id)
   
    
    if start is not None and end is not None:
        query = query.where(
            Measurement.timestamp >= start,
            Measurement.timestamp <= end,
        ).order_by(Measurement.timestamp.desc())
    else:
        #Muuten uusimmat "limit" mittausta
        query = query.order_by(Measurement.timestamp.desc()).limit(limit)

    measurements = session.exec(query).all()

    return SensorWithMeasurements(
        id=sensor.id,
        name=sensor.name,
        section=sensor.section,
        status=sensor.status,
        measurements=measurements,
    )


# SECTIONS


def get_sensors_by_section(session: Session, section: str) -> List[SensorBySection]:

    sensors_in_section = session.exec(
        select(SensorOut).where(SensorOut.section == section)
    ).all()

    result: List[SensorBySection] = []

    for s in sensors_in_section:
        last_measurement = session.exec(
            select(Measurement)
            .where(Measurement.sensor_id == s.id)
            .order_by(Measurement.timestamp.desc())
            .limit(1)
        ).first()

        result.append(
            SensorBySection(
                id=s.id,
                section=s.section,
                status=s.status,
                last_temperature=last_measurement.temperature if last_measurement else None,
                last_timestamp=last_measurement.timestamp if last_measurement else None,
            )
        )
    return result



#STATUS-CHANGES


def get_statuschanges_by_sensorId(
        session: Session, sensor_id: int) -> List[StatusChange]:
    
    sensor = session.get(SensorOut, sensor_id)
    if sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'sensor with id {sensor_id} not found.'
        )
    
    changes = session.exec(
        select(StatusChange).where(StatusChange.sensor_id == sensor_id)
    ).all()

    return changes


#ERROR-EVENTIT (Graafia varten)

def get_error_events(
    session: Session, sensor_id: Optional[int] = None) -> List[ErrorEvent]:

    query = select(StatusChange).where(StatusChange.new_status == "error")

    if sensor_id is not None:
        query = query.where(StatusChange.sensor_id == sensor_id)
    
    rows = session.exec(query).all()

    return [
        ErrorEvent(sensor_id=r.sensor_id, timestamp=r.timestamp)
        for r in rows
    ]


#MEASUREMENTS

def create_measurement(
        session: Session, measurement_in: MeasurementIn) -> MeasurementOut:
    sensor = session.get(SensorOut, measurement_in.sensor_id)
    if sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Sensor with id {measurement_in.sensor_id} not found.'
        )
    
    if sensor.status == "error":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Measurement cannot be added because the sensor is in 'error' state."
        )
    
    
    ts = measurement_in.timestamp or datetime.now()

    db_measurement = Measurement(
        sensor_id=measurement_in.sensor_id,
        temperature=measurement_in.temperature,
        timestamp=ts,
    )

    session.add(db_measurement)
    session.commit()
    session.refresh(db_measurement)

    return MeasurementOut(
        id=db_measurement.id,
        sensor_id=db_measurement.sensor_id,
        temperature=db_measurement.temperature,
        timestamp=db_measurement.timestamp,
    )


def delete_measurement_by_id(
    session: Session, measurement_id: int) -> None:
    
    measurement = session.get(Measurement, measurement_id)
    if measurement is None:
        raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail=f'Measurement with id {measurement_id} not found.',   
        )

    session.delete(measurement)
    session.commit()
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)