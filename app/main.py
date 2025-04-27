from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.database import db
from services.rest_service import router
from services.grpc_service import serve
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.create_pool()

    grpc_task = asyncio.create_task(serve())

    yield

    grpc_task.cancel()
    try:
        await grpc_task
    except asyncio.CancelledError:
        pass

    await db.pool.close()

app = FastAPI(lifespan=lifespan)
app.include_router(router)
