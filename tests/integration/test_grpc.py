# from app.grpc_package import med_schedule_pb2

# async def test_grpc_create_schedule(grpc_stub):
#     request = med_schedule_pb2.CreateScheduleRequest(
#         user_id=1,
#         name="Test Medication",
#         frequency=2,
#         duration=30
#     )
#     response = await grpc_stub.CreateSchedule(request)
#     assert response.schedule_id

# async def test_grpc_get_schedule_detail(grpc_stub):
#     create_request = med_schedule_pb2.CreateScheduleRequest(
#         user_id=1,
#         name="Test Medication",
#         frequency=2,
#         duration=30
#     )
#     create_response = await grpc_stub.CreateSchedule(create_request)
    
#     detail_request = med_schedule_pb2.ScheduleDetailRequest(
#         user_id=1,
#         schedule_id=int(create_response.schedule_id)
#     )
#     detail_response = await grpc_stub.GetScheduleDetail(detail_request)
#     assert detail_response.name == "Test Medication"
