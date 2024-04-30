from typing import AsyncGenerator, Optional, Union

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from core.database import get_session
from core.auth import oauth2_schema
from core.configs import settings
from models.usuario_model import UsuarioModel


class TokenData(BaseModel):
    username: Optional[str] = None
    

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with get_session() as session:
        yield session
        

async def get_current_user(db: AsyncSession = Depends(get_session), 
                           token: str = Depends(oauth2_schema)) -> UsuarioModel:
    
    credential_exeption: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Não foi possovél autenticar a credencial',
        headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payloand = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )
        
        username: Union[str, None] = payloand.get("sub")
        if username is None:
            raise credential_exeption
        
        token_data: TokenData = TokenData(username=username)
    except JWTError:
        raise credential_exeption
    
    async with db as session: 
        query = select(UsuarioModel).filter(UsuarioModel.id == str(token_data.username))
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()
        
        if usuario is None:
            raise credential_exeption
        
        return usuario