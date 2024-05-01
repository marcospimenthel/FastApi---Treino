from typing import AsyncGenerator, Optional, Union

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from core.database import get_session
from core.auth import oauth2_schema
from core.configs import settings
from models.usuario_model import UsuarioBase  # Corrigido o nome da classe importada

class TokenData(BaseModel):
    username: Optional[str] = None
    

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Função assíncrona para obter uma sessão do banco de dados.
    Utiliza a função get_session para obter uma sessão assíncrona e a retorna usando um gerador assíncrono.
    """
    async with get_session() as session:
        yield session
        

async def get_current_user(token: str = Depends(oauth2_schema),
                           db: AsyncSession = Depends(get_session)) -> UsuarioBase:  # Corrigido o tipo de retorno
    """
    Função assíncrona para obter o usuário atual com base no token JWT fornecido.
    Verifica se o token é válido e decodifica seu payload para obter o identificador do usuário.
    Em seguida, busca o usuário no banco de dados e o retorna, se encontrado.
    """
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Não foi possível autenticar as credenciais',
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )
        username: Union[str, None] = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    
    async with db as session: 
        query = select(UsuarioBase).filter(UsuarioBase.id == str(token_data.username))
        result = await session.execute(query)
        usuario: UsuarioBase = result.scalars().unique().one_or_none()
        
        if usuario is None:
            raise credential_exception
        
        return usuario
