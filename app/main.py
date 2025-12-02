from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routers import measurements, sensors, stats, status_changes
from .database.database import create_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(sensors.router)
app.include_router(measurements.router)
app.include_router(status_changes.router)
app.include_router(stats.router)

































    