from fastapi import APIRouter, status, Depends
from sqlmodel import Session
from ..database.database import get_session
from ..database import crud
from ..database.models import MeasurementOut, MeasurementIn



router = APIRouter(prefix="/measurements", tags=["Measurements"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=MeasurementOut)
def create_measurement(*, session: Session = Depends(get_session), measurement_in: MeasurementIn):
    return crud.create_measurement(session, measurement_in)


@router.delete("/{measurement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_measurement_by_id(*, session: Session = Depends(get_session), measurement_id: int):
    
    crud.delete_measurement_by_id(session, measurement_id)
    return None

