# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.ext.asyncio import AsyncEngine
# from sqlalchemy.ext.asyncio import AsyncSession

# from core.configs import settings

# engine: AsyncEngine = create_async_engine(settings.DB_URL)

# Session: sessionmaker = sessionmaker(
#     autoflush=False,
#     autocommit=False,
#     expire_on_commit=False,
#     class_=AsyncSession,
#     blind=engine
# ) 

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from core.configs import settings

engine = create_async_engine(settings.DB_URL, echo=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)

def get_session() -> AsyncSession:
    return SessionLocal()



