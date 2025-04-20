from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import db
from rest_service import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.create_pool()
    yield
    await db.pool.close()

app = FastAPI(lifespan=lifespan)
app.include_router(router)
