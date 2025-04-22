from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.database import db
from services.rest_service import router
import threading
from services.grpc_service import serve
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.create_pool()

    grpc_thread = threading.Thread(target=asyncio.run, args=(serve(),), daemon=True)
    grpc_thread.start()

    yield
    await db.pool.close()

app = FastAPI(lifespan=lifespan)
app.include_router(router)
