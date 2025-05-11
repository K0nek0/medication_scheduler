from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.settings import settings
from typing import Optional

class Database:
    def __init__(self):
        self.engine = None
        self.async_session: Optional[AsyncSession] = None

    async def create_engine(self):
        if not self.engine:
            self.engine = create_async_engine(
                settings.database_url,
                pool_size=5,
                max_overflow=20,
                pool_timeout=10
            )
            self.async_session = sessionmaker(
                self.engine, expire_on_commit=False, class_=AsyncSession
            )
    
    async def close_engine(self):
        if self.engine:
            await self.engine.dispose()
            self.engine = None
            self.async_session = None

db = Database()
