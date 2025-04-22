from concurrent import futures
import grpc
from grpc_package import med_schedule_pb2_grpc
from grpc_package.med_schedule_pb2 import (
    ScheduleResponse,
    UserSchedulesResponse,
    ScheduleDetailResponse,
    NextTakingsResponse,
    NextTaking
)
from core.handler import create_schedule, get_schedules, get_schedule_detail, get_takings
from models.med_schedule_model import MedicationSchedule
from datetime import time
from core.utils import generate_schedule_id
from db.database import db

class MedicationScheduleServicer(med_schedule_pb2_grpc.MedicationScheduleServiceServicer):
    async def CreateSchedule(self, request, context):
        new_schedule = MedicationSchedule(
            schedule_id=generate_schedule_id(user_id=request.user_id),
            user_id=request.user_id,
            name=request.name,
            frequency=request.frequency,
            duration=request.duration,
            start_time=time(8, 0),
            end_time=time(22, 0)
        )
        await create_schedule(new_schedule)
        return ScheduleResponse(schedule_id=new_schedule.schedule_id)

    async def GetUserSchedules(self, request, context):
        schedule_ids = await get_schedules(request.user_id)
        return UserSchedulesResponse(schedule_ids=schedule_ids)

    async def GetScheduleDetail(self, request, context):
        detail = await get_schedule_detail(request.user_id, request.schedule_id)
        if not detail:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Расписание не найдено")
            return ScheduleDetailResponse()
        
        from core.utils import calculate_schedule_times
        times = calculate_schedule_times(detail['frequency'], detail['start_time'], detail['end_time'])
        return ScheduleDetailResponse(
            name=detail['name'],
            frequency=detail['frequency'],
            duration=detail['duration'],
            schedule=times
        )

    async def GetNextTakings(self, request, context):
        takings = await get_takings(request.user_id)
        return NextTakingsResponse(takings=[NextTaking(name=t['name'], time=t['time']) for t in takings])

async def serve():
    await db.create_pool()
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    med_schedule_pb2_grpc.add_MedicationScheduleServiceServicer_to_server(
        MedicationScheduleServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    await server.start()
    print("gRPC сервер запущен на порту 50051")
    await server.wait_for_termination()
