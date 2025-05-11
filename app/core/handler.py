from datetime import datetime, timedelta, time
from sqlalchemy import select, insert
from app.models.models_auto import ScheduleCreate
from app.db.database import db
from app.core.utils import calculate_schedule_times
from app.models.schedule_model import Schedule
from app.core.utils import generate_schedule_id

async def create_schedule(schedule: ScheduleCreate) -> int:
    async with db.async_session() as session:
        schedule_data = {
            "schedule_id": generate_schedule_id(user_id=schedule.user_id),
            "user_id": schedule.user_id,
            "name": schedule.name,
            "frequency": schedule.frequency,
            "duration": schedule.duration,
            "start_time": time(8, 0),
            "end_time": time(22, 0)
        }
        stmt = insert(Schedule).values(**schedule_data)
        await session.execute(stmt)
        await session.commit()
        return schedule_data["schedule_id"]

async def get_schedule_detail(user_id, schedule_id):
    async with db.async_session() as session:
        result = await session.execute(
            select(
                Schedule.name,
                Schedule.frequency,
                Schedule.duration,
                Schedule.start_time,
                Schedule.end_time
            ).where(
                (Schedule.user_id == user_id) & 
                (Schedule.schedule_id == schedule_id)
            )
        )
        detail = result.first()
        return {
            "name": detail.name,
            "frequency": detail.frequency,
            "duration": detail.duration,
            "start_time": detail.start_time,
            "end_time": detail.end_time
        }

async def get_schedules(user_id):
    async with db.async_session() as session:
        result = await session.execute(
            select(Schedule.schedule_id).where(Schedule.user_id == user_id)
        )
        return result.scalars().all()

async def get_takings(user_id):
    async with db.async_session() as session:
        result = await session.execute(
            select(
                Schedule.name,
                Schedule.frequency,
                Schedule.start_time,
                Schedule.end_time
            ).where(Schedule.user_id == user_id)
        )
        schedules = result.all()

    next_takings = []
    now = datetime.now()
    one_hour_later = now + timedelta(hours=1)

    for schedule in schedules:
        times = calculate_schedule_times(schedule.frequency, schedule.start_time, schedule.end_time)
        for t in times:
            time_obj = datetime.strptime(t, '%H:%M').time()
            if now.time() <= time_obj <= one_hour_later.time():
                next_takings.append({
                    "name": schedule.name,
                    "time": t
                })

    return next_takings
