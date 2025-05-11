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
from app.models.models_auto import ScheduleCreate
# from logger.business_logger import business_logger

class MedicationScheduleServicer(med_schedule_pb2_grpc.MedicationScheduleServiceServicer):
    # @business_logger("grpc_create_schedule")
    async def CreateSchedule(self, request, context):
        schedule_data = ScheduleCreate(
            user_id=request.user_id,
            name=request.name,
            frequency=request.frequency,
            duration=request.duration
        )
        schedule_id = await create_schedule(schedule_data)
        return ScheduleResponse(schedule_id=str(schedule_id))

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

    # @business_logger("grpc_get_user_schedules")
    async def GetUserSchedules(self, request, context):
        schedule_ids = await get_schedules(request.user_id)
        return UserSchedulesResponse(schedule_ids=schedule_ids)

    # @business_logger("grpc_get_next_takings")
    async def GetNextTakings(self, request, context):
        takings = await get_takings(request.user_id)
        return NextTakingsResponse(takings=[NextTaking(name=t['name'], time=t['time']) for t in takings])
