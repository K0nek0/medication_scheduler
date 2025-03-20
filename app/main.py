from fastapi import FastAPI, HTTPException, Query
from services import create_schedule, get_schedules, get_schedule_detail, calculate_schedule_times, get_next_takings
from models import MedicationSchedule
from datetime import time

app = FastAPI()

@app.post("/schedule")
async def create_new_schedule(schedule):
    new_schedule = MedicationSchedule(
        name=schedule.name,
        frequency=schedule.frequency,
        duration=schedule.duration,
        user_id=schedule.user_id
    )
    create_schedule(new_schedule)
    return {"schedule_id": new_schedule.schedule_id}

@app.get("/schedules")
async def get_user_schedules(user_id):
    return get_schedules(user_id)

@app.get("/schedule")
async def get_schedule(user_id, schedule_id):
    detail = get_schedule_detail(user_id, schedule_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Расписание не найдено")

    times = calculate_schedule_times(detail['frequency'], detail['start_time'], detail['end_time'])
    return {
        "name": detail['name'],
        "frequency": detail['frequency'],
        "duration": detail['duration'],
        "schedule": times
    }

@app.get("/next_takings")
async def get_next_takings(user_id):
    takings = get_next_takings(user_id)
    return takings
