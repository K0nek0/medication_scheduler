import pytest
import asyncpg
from app.settings import settings

@pytest.fixture(scope="session", autouse=True)
async def prepare_test_db():
    conn = await asyncpg.connect(settings.database_url)
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS schedules_test (
            schedule_id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            frequency TEXT NOT NULL,
            duration INTEGER NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL
        )
    """)
    await conn.close()

@pytest.fixture(scope="function", autouse=True)
async def clean_tables(db_pool):
    async with db_pool.acquire() as conn:
        await conn.execute("TRUNCATE TABLE schedules RESTART IDENTITY")
