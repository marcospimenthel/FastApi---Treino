from typing import ClassVar
from pydantic_settings import BaseSettings
from sqlalchemy.orm import declarative_base

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://postgres:roottoor@localhost:5432/postgres"
    DBBaseModel: ClassVar = declarative_base()
    
    JWT_SECRET: str ='hScdJLik3AogwrgVrSLAFywr_kvWEJ-XZOGoFw_bkUE'
    ALGORITHM: str = 'HS256'
    
    ACCESS_TOKEN_MINUTES: int = 60 * 24 * 7
    
    class Config:
        case_sensitive = True

settings: Settings = Settings()
