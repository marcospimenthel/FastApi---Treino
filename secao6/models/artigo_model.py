from pydantic import BaseModel
from pydantic.class_validators import validator
from typing import List, Optional
from datetime import datetime

class ArtigoBase(BaseModel):
    titulo: str
    conteudo: str

class ArtigoCreate(ArtigoBase):
    pass

class Artigo(ArtigoBase):
    id: int
    autor_id: int
    data_publicacao: Optional[datetime]

    class Config:
        orm_mode = True

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_id

    @classmethod
    def validate_id(cls, v):
        if v < 0:
            raise ValueError("id deve ser um número positivo")
        return v

    @validator("titulo")
    def titulo_must_contain_title(cls, v):
        if "title" not in v.lower():
            raise ValueError("o título deve conter a palavra 'title'")
        return v

    @validator("conteudo")
    def conteudo_not_empty(cls, v):
        if not v.strip():
            raise ValueError("o conteúdo não pode estar vazio")
        return v
