import requests

# # Создание расписания
# response = requests.post(
#     "http://127.0.0.1:8000/schedule",
#     json={
#         "user_id": "1234523",
#         "name": "Таблетки_1",
#         "frequency": "1 раз в день",
#         "duration": "месяц"
#     }
# )
# print(response.json())

# # Получение списка расписаний
# response = requests.get("http://127.0.0.1:8000/schedules?user_id=12345")
# print(response.json())

# # Получение деталей расписания
# response = requests.get(
#     "http://127.0.0.1:8000/schedule",
#     params={"user_id": "1234523", "schedule_id": "1234523195051"}
# )
# print(response.json())

# Получение ближайших приемов
response = requests.get("http://127.0.0.1:8000/next_takings?user_id=1234523")
print(response.json())
