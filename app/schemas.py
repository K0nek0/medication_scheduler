from pydantic import BaseModel

class ScheduleCreate(BaseModel):
    name: str
    frequency: str
    duration: str
    user_id: str

class ScheduleResponse(BaseModel):
    schedule_id: str

class ScheduleDetail(BaseModel):
    name: str
    frequency: str
    duration: str
    schedule: list[str]

class NextTakings(BaseModel):
    name: str
    time: str
    