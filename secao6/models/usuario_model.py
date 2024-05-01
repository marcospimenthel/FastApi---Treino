from pydantic import BaseModel
from typing import List, Optional
from .artigo_model import ArtigoBase


class UsuarioBase(BaseModel):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: str
    senha: str
    eh_admin: bool

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id: int
    artigos: List[ArtigoBase]

    class Config:
        orm_mode = True
