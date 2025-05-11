import asyncpg
from app.settings import settings
from typing import Optional

class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def create_pool(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(
                dsn=settings.database_url,
                min_size=5,
                max_size=20,
                timeout=10
            )
    
    async def close_pool(self):
        if self.pool:
            await self.pool.close()
            self.pool = None

db = Database()
