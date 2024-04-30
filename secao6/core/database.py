# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.ext.asyncio import AsyncEngine
# from sqlalchemy.ext.asyncio import AsyncSession

# from core.configs import settings

# engine: AsyncEngine = create_async_engine(settings.DB_URL)

# Session: AsyncSession = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     expire_on_commit=False,
#     class_=AsyncSession,
#     bind=engine
# )

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.configs import settings

engine = create_async_engine(settings.DB_URL)

# Crie o engine assíncrono
engine = create_async_engine(settings.DB_URL, echo=True)

# Use async_sessionmaker para criar a fábrica de sessões assíncronas
Session = sessionmaker(
    engine, 
    class_=AsyncSession,
    expire_on_commit=False, 
    autoflush=False)

def get_session() -> AsyncSession:
    return Session()

__all__ = ["engine", "Session"]




