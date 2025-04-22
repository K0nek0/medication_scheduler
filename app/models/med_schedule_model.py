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
