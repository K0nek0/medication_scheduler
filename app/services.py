from datetime import datetime, timedelta
from models import MedicationSchedule
from database import db
from utils import calculate_schedule_times

async def create_schedule(schedule: MedicationSchedule):
    async with db.pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO schedules (schedule_id, user_id, name, frequency, duration, start_time, end_time)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
        """, *(
            schedule.schedule_id, schedule.user_id,
            schedule.name, schedule.frequency, schedule.duration,
            schedule.start_time, schedule.end_time
        ))

async def get_schedules(user_id):
    async with db.pool.acquire() as conn:
        schedules = await conn.fetch("SELECT schedule_id FROM schedules WHERE user_id = $1", user_id)
        return [s['schedule_id'] for s in schedules]

async def get_schedule_detail(user_id, schedule_id):
    async with db.pool.acquire() as conn:
        detail = await conn.fetchrow("""
            SELECT name, frequency, duration, start_time, end_time FROM schedules
            WHERE user_id = $1 AND schedule_id = $2
        """, user_id, schedule_id)
        return detail

async def get_takings(user_id):
    async with db.pool.acquire() as conn:
        schedules = await conn.fetch("""
            SELECT name, frequency, start_time, end_time FROM schedules
            WHERE user_id = $1
        """, user_id)

    next_takings = []
    now = datetime.now()
    one_hour_later = now + timedelta(hours=1)

    for schedule in schedules:
        times = calculate_schedule_times(schedule['frequency'], schedule['start_time'], schedule['end_time'])
        for t in times:
            time_obj = datetime.strptime(t, '%H:%M').time()
            if now.time() <= time_obj <= one_hour_later.time():
                next_takings.append({
                    "name": schedule['name'],
                    "time": t
                })

    return next_takings
