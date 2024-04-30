from core.configs import settings
from sqlalchemy import Column, Integer, String
from typing import Type


class CursoModel(settings.DBBaseModel):
    __tablename__ = 'cursos'
    
    id: Column = Column(Integer, primary_key=True, autoincrement=True)
    # titulo: Column[str] = Column(String(100))
    # aulas: Column[int] = Column(Integer)
    # horas: Column[int] = Column(Integer)
    titulo = Column(String(100))
    aulas = Column(Integer)
    horas = Column(Integer)