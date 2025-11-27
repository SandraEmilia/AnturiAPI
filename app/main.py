from fastapi import FastAPI
from .routers import measurements, sensors, stats, status_changes

app = FastAPI()

app.include_router(sensors.router)
app.include_router(measurements.router)
app.include_router(status_changes.router)
app.include_router(stats.router)

































    