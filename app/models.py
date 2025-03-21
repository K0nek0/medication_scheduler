from pydantic import BaseModel
from datetime import time

class MedicationSchedule(BaseModel):
    schedule_id: int
    user_id: int
    name: str
    frequency: str
    duration: str
    start_time: time
    end_time: time

class ScheduleCreate(BaseModel):
    user_id: int
    name: str
    frequency: str
    duration: str

class ScheduleResponse(BaseModel):
    schedule_id: int

class ScheduleDetail(BaseModel):
    name: str
    frequency: str
    duration: str
    schedule: list[str]

class NextTakings(BaseModel):
    name: str
    time: str
