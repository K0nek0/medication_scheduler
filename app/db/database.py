import asyncpg
from settings import settings

class Database:
    def __init__(self):
        self.pool: asyncpg.Pool = None

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(
            dsn=settings.database_url,
            min_size=5,
            max_size=20
        )

db = Database()
