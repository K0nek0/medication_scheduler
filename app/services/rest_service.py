from fastapi import HTTPException, Query, APIRouter
from core.handler import create_schedule, get_schedules, get_schedule_detail, calculate_schedule_times, get_takings
from models.models_auto import ScheduleCreate, ScheduleResponse, ScheduleDetail, NextTakings
from models.med_schedule_model import MedicationSchedule
from typing import List
from datetime import time
from core.utils import generate_schedule_id
# from logger.business_logger import business_logger

router = APIRouter(prefix="/api/v1")

@router.post("/schedule", response_model=ScheduleResponse)
# @business_logger("create_schedule")
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

@router.get("/schedules", response_model=List[int])
# @business_logger("get_user_schedules")
async def get_user_schedules(user_id: int = Query(..., description="ID пользователя")):
    return await get_schedules(user_id)

@router.get("/schedule", response_model=ScheduleDetail)
# @business_logger("get_schedule_detail")
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

@router.get("/next_takings", response_model=List[NextTakings])
# @business_logger("get_next_takings")
async def get_next_takings(user_id: int = Query(..., description="ID пользователя")):
    return await get_takings(user_id)
