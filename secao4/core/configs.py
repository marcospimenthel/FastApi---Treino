
# from pydantic import BaseSettings
# from sqlalchemy.ext.declarative import declarative_base


# class Settings(BaseSettings):
#     """
#     Cnfigurações gerais usadas na aplicação
#     """
#     API_V1_STR: str = '/api/v1'
#     DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/api"
#     DBBaseModel = declarative_base()
    
#     class config:
#         case_sensitive = True
        
# settings = Settings()

from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/api"
    DBBaseModel = declarative_base()

    class Config:
        case_sensitive = True

settings = Settings()

