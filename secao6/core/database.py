from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from core.configs import settings

# Crie o engine assíncrono com echo=True para mostrar instruções SQL geradas
engine = create_async_engine(settings.DB_URL, echo=True)

# Use async_sessionmaker para criar a fábrica de sessões assíncronas
Session = sessionmaker(
    engine, 
    class_=AsyncSession,
    expire_on_commit=False, 
    autoflush=False)

def get_session() -> AsyncSession:
    """
    Função para obter uma sessão do banco de dados.
    Retorna uma instância de AsyncSession.
    """
    try:
        return Session()
    except SQLAlchemyError as e:
        # Tratamento de erro caso a conexão com o banco de dados falhe
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise

__all__ = ["engine", "Session", "get_session"]
