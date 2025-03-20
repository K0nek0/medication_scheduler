from datetime import datetime, timedelta, time
from typing import List, Dict
from models import MedicationSchedule
from database import get_db

def create_schedule(schedule: MedicationSchedule):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO schedules (schedule_id, name, frequency, duration, user_id, start_time, end_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        schedule.schedule_id, schedule.name, schedule.frequency, 
        schedule.duration, schedule.user_id, schedule.start_time, schedule.end_time
    ))
    conn.commit()
    cur.close()
    conn.close()

def get_schedules(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT schedule_id FROM schedules WHERE user_id = %s", (user_id,))
    schedules = cur.fetchall()
    cur.close()
    conn.close()
    return [s['schedule_id'] for s in schedules]

def get_schedule_detail(user_id, schedule_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT name, frequency, duration, start_time, end_time FROM schedules
        WHERE user_id = %s AND schedule_id = %s
    """, (user_id, schedule_id))
    detail = cur.fetchone()
    cur.close()
    conn.close()
    return detail

def calculate_schedule_times(frequency, start_time, end_time):
    times = []
    current_time = datetime.now().replace(
        hour=start_time.hour, 
        minute=start_time.minute, 
        second=0, 
        microsecond=0
    )
    end_time = datetime.now().replace(
        hour=end_time.hour, 
        minute=end_time.minute, 
        second=0, 
        microsecond=0
    )

    if frequency == "1 раз в день":
        times.append(current_time.strftime('%H:%M'))
    elif frequency == "каждый час":
        while current_time <= end_time:
            times.append(current_time.strftime('%H:%M'))
            current_time += timedelta(hours=1)
    elif frequency == "каждые 15 минут":
        while current_time <= end_time:
            times.append(current_time.strftime('%H:%M'))
            current_time += timedelta(minutes=15)

    return times

def get_next_takings(user_id: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT name, frequency, start_time, end_time FROM schedules
        WHERE user_id = %s
    """, (user_id,))
    schedules = cur.fetchall()
    cur.close()
    conn.close()

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
