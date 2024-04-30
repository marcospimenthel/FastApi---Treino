
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session as create_session

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = create_session()
    try:
        yield session 
    finally:
        await session.close()


