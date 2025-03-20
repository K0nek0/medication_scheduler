from datetime import datetime, time

class MedicationSchedule:
    def __init__(self, name, frequency, duration, user_id):
        self.name = name
        self.frequency = frequency
        self.duration = duration
        self.user_id = user_id
        self.start_time = time(8, 0)
        self.end_time = time(22, 0)
        self.schedule_id = self.generate_schedule_id()

    def generate_schedule_id(self):
        return f"{self.user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    