# tests/conftest.py
import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import make_app
from app.db.database import db

# @pytest.fixture(scope="session")
# def event_loop():
#     loop = asyncio.get_event_loop()
#     yield loop
#     loop.close()

# @pytest.fixture(scope="session", autouse=True)
# async def initialize_db():
#     await db.create_pool()
    
#     async with db.pool.acquire() as conn:
#         await conn.execute("""
#             CREATE TABLE IF NOT EXISTS schedules (
#                 schedule_id bigint PRIMARY KEY,
#                 user_id bigint NOT NULL,
#                 name varchar(255) NOT NULL,
#                 frequency varchar(255) NOT NULL,
#                 duration varchar(255) NOT NULL,
#                 start_time time NOT NULL,
#                 end_time time NOT NULL
#             )
#         """)
#     yield
    
#     await db.close_pool()

@pytest.fixture(scope="session", autouse=True)
async def init_db():
    if not db.pool:
        await db.create_pool() 

@pytest.fixture
def app():
    return make_app()

@pytest.fixture
def client(app):
    return TestClient(app)

@pytest.fixture
async def db_connection():
    conn = await db.pool.acquire()
    try:
        yield conn
    finally:
        await db.pool.release(conn)
