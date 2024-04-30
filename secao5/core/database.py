
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from core.configs import Settings

# Instancie a classe Settings
settings = Settings()

# Crie o engine assíncrono
engine = create_async_engine(settings.DB_URL, echo=True)

# Use async_sessionmaker para criar a fábrica de sessões assíncronas
SessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession,
    expire_on_commit=False, 
    autoflush=False)

def get_session() -> AsyncSession:
    return SessionLocal()

__all__ = ["engine", "SessionLocal"]
