from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import AsyncSessionLocal


async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
