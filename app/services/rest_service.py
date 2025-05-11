from fastapi import HTTPException, Query, APIRouter
from app.core.handler import create_schedule, get_schedules, get_schedule_detail, get_takings
from app.core.utils import calculate_schedule_times
from app.models.models_auto import ScheduleCreate, ScheduleResponse, ScheduleDetail, NextTakings
from typing import List
# from logger.business_logger import business_logger

router = APIRouter(prefix="/api/v1")

@router.post("/schedule", response_model=ScheduleResponse)
# @business_logger("create_schedule")
async def create_new_schedule(schedule: ScheduleCreate):
    schedule_id = await create_schedule(schedule)
    return {"schedule_id": schedule_id}

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

@router.get("/schedules", response_model=List[int])
# @business_logger("get_user_schedules")
async def get_user_schedules(user_id: int = Query(..., description="ID пользователя")):
    return await get_schedules(user_id)

@router.get("/next_takings", response_model=List[NextTakings])
# @business_logger("get_next_takings")
async def get_next_takings(user_id: int = Query(..., description="ID пользователя")):
    return await get_takings(user_id)
