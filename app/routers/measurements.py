from fastapi import APIRouter, status
from ..database import crud
from ..database.models import MeasurementBase

router = APIRouter(prefix="/measurements", tags=["Measurements"])

@router.delete("/{measurement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_measurement_by_id(measurement_id: int):
    return crud.delete_measurement_by_id(measurement_id)

