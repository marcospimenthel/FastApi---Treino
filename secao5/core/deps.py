# from typing import AsyncGenerator
# from sqlalchemy.ext.asyncio import AsyncSession
# from core.database import get_session
# from core.configs import Settings

# async def get_session() -> AsyncGenerator[AsyncSession, None]:
#     session = get_session()
#     try:
#         yield session 
#     finally:
#         await session.close()
        
        
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with get_session() as session:
        yield session
