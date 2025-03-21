from fastapi import FastAPI, HTTPException, Query
from services import create_schedule, get_schedules, get_schedule_detail, calculate_schedule_times, get_takings
from models import MedicationSchedule, ScheduleCreate, ScheduleResponse, ScheduleDetail, NextTakings
from typing import List
from contextlib import asynccontextmanager
from database import db
from datetime import time
from utils import generate_schedule_id

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.create_pool()
    yield
    await db.pool.close()

app = FastAPI(lifespan=lifespan)

@app.post("/schedule", response_model=ScheduleResponse)
async def create_new_schedule(schedule: ScheduleCreate):
    new_schedule = MedicationSchedule(
        schedule_id = generate_schedule_id(user_id=schedule.user_id),
        user_id=schedule.user_id,
        name=schedule.name,
        frequency=schedule.frequency,
        duration=schedule.duration,
        start_time = time(8, 0),
        end_time = time(22, 0)
    )
    await create_schedule(new_schedule)
    return {"schedule_id": new_schedule.schedule_id}

@app.get("/schedules", response_model=List[int])
async def get_user_schedules(user_id: int = Query(..., description="ID пользователя")):
    return await get_schedules(user_id)

@app.get("/schedule", response_model=ScheduleDetail)
async def get_schedule(
    user_id: int = Query(..., description="ID пользователя"),
    schedule_id: int = Query(..., description="ID расписания")):

    detail = await get_schedule_detail(user_id, schedule_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Расписание не найдено")

    times = calculate_schedule_times(detail['frequency'], detail['start_time'], detail['end_time'])
    return {
        "name": detail['name'],
        "frequency": detail['frequency'],
        "duration": detail['duration'],
        "schedule": times
    }

@app.get("/next_takings", response_model=List[NextTakings])
async def get_next_takings(user_id: int = Query(..., description="ID пользователя")):
    return await get_takings(user_id)
