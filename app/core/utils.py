from datetime import datetime, timedelta

def generate_schedule_id(user_id):
    return int(f"{user_id}{datetime.now().strftime('%H%M%S')}")

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
