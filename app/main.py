from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import db
from app.services.rest_service import router
from app.services.grpc_service import MedicationScheduleServicer
from app.grpc_package import med_schedule_pb2_grpc
import grpc
from concurrent import futures
import asyncio
from typing import AsyncGenerator, Any
# from logger.logging_config import configure_logging
# from logger.logging_middleware import APILoggingMiddleware

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    med_schedule_pb2_grpc.add_MedicationScheduleServiceServicer_to_server(
        MedicationScheduleServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    await server.start()
    print("gRPC сервер запущен на порту 50051")
    await server.wait_for_termination()
    
@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncGenerator[dict[str, Any], None]:
    try:
        await db.create_pool()
        if not db.pool:
            raise RuntimeError("Не удалось создать пул соединений с БД")
    except Exception as e:
        print(f"Ошибка инициализации БД: {e}")
        raise

    grpc_task = asyncio.create_task(serve())
    
    yield

    grpc_task.cancel()
    try:
        await grpc_task
    except asyncio.CancelledError:
        pass

    await db.close_pool()

def make_app() -> FastAPI:
    app = FastAPI(lifespan=_lifespan)

    # configure_logging()

    # app.add_middleware(APILoggingMiddleware)
    app.include_router(router)
    return app
