import grpc
from app.grpc_package import med_schedule_pb2, med_schedule_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = med_schedule_pb2_grpc.MedicationScheduleServiceStub(channel)

request = med_schedule_pb2.ScheduleCreateRequest(
    user_id=1,
    name="Аспирин",
    frequency="3 раза в день",
    duration="7 дней"
)

response = stub.CreateSchedule(request)
print(f"Создано расписание с ID: {response.schedule_id}")
