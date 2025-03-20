import requests

# Создание расписания
response = requests.post(
    "http://127.0.0.1:8000/schedule",
    json={
        "name": "Аспирин",
        "frequency": "каждый час",
        "duration": "2 недели",
        "user_id": "12345"
    }
)
print(response.json())

# # Получение списка расписаний
# response = requests.get("http://127.0.0.1:8000/schedules?user_id=12345")
# print(response.json())

# # Получение деталей расписания
# response = requests.get(
#     "http://127.0.0.1:8000/schedule",
#     params={"user_id": "12345", "schedule_id": "12345_20250319174901"}
# )
# print(response.json())

# # Получение ближайших приемов
# response = requests.get("http://127.0.0.1:8000/next_takings?user_id=12345")
# print(response.json())
