from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.database import db
from services.rest_service import router
from services.grpc_service import MedicationScheduleServicer
from grpc_package import med_schedule_pb2_grpc
import grpc
from concurrent import futures
import asyncio
# from logger.logging_config import configure_logging
# from logger.logging_middleware import APILoggingMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.create_pool()

    async def serve():
        server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
        med_schedule_pb2_grpc.add_MedicationScheduleServiceServicer_to_server(
            MedicationScheduleServicer(), server
        )
        server.add_insecure_port('[::]:50051')
        await server.start()
        print("gRPC сервер запущен на порту 50051")
        await server.wait_for_termination()

    grpc_task = asyncio.create_task(serve())
    
    yield

    grpc_task.cancel()
    try:
        await grpc_task
    except asyncio.CancelledError:
        pass

    await db.pool.close()

app = FastAPI(lifespan=lifespan)

# configure_logging()

# app.add_middleware(APILoggingMiddleware)
app.include_router(router)
