from app.grpc_package import med_schedule_pb2_grpc
from app.grpc_package.med_schedule_pb2 import (
    ScheduleResponse,
    UserSchedulesResponse,
    ScheduleDetailResponse,
    NextTakingsResponse,
    NextTaking
)
from app.core.handler import create_schedule, get_schedules, get_schedule_detail, get_takings
from app.core.utils import calculate_schedule_times
from app.models.med_schedule_model import MedicationSchedule
from datetime import time
from app.core.utils import generate_schedule_id
from app.db.database import db
# from logger.business_logger import business_logger

class MedicationScheduleServicer(med_schedule_pb2_grpc.MedicationScheduleServiceServicer):
    # @business_logger("grpc_create_schedule")
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

    # @business_logger("grpc_get_user_schedules")
    async def GetUserSchedules(self, request, context):
        schedule_ids = await get_schedules(request.user_id)
        return UserSchedulesResponse(schedule_ids=schedule_ids)

    # @business_logger("grpc_get_schedule_detail")
    async def GetScheduleDetail(self, request, context):
        detail = await get_schedule_detail(request.user_id, request.schedule_id)
        if not detail:
            context.set_details("Расписание не найдено")
            return ScheduleDetailResponse()
        
        times = calculate_schedule_times(detail['frequency'], detail['start_time'], detail['end_time'])
        return ScheduleDetailResponse(
            name=detail['name'],
            frequency=detail['frequency'],
            duration=detail['duration'],
            schedule=times
        )

    # @business_logger("grpc_get_next_takings")
    async def GetNextTakings(self, request, context):
        takings = await get_takings(request.user_id)
        return NextTakingsResponse(takings=[NextTaking(name=t['name'], time=t['time']) for t in takings])
