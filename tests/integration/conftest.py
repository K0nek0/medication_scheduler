import pytest
import asyncpg
from fastapi.testclient import TestClient
from app.main import make_app
from app.db.database import db
from app.settings import settings
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module")
async def db_pool():
    pool = await asyncpg.create_pool(settings.database_url)
    yield pool
    await pool.close()

@pytest.fixture(scope="module")
async def test_app(db_pool):
    app = make_app()
    app.state.db_pool = db_pool
    yield app

@pytest.fixture(scope="module")
def test_client(test_app):
    with TestClient(test_app) as client:
        yield client
