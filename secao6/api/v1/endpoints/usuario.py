from typing import List, Optional

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UsuarioBase  # Corrigindo a importação

from core.deps import get_session, get_current_user
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso

from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

# GET Logado
@router.get('/logado', response_model=UsuarioBase)
def get_logado(usuario_logado: UsuarioBase = Depends(get_current_user)):
    return usuario_logado

# POST / Signup
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioBase)
async def post_usuario(usuario: UsuarioBase, db: AsyncSession = Depends(get_session)):
    novo_usuario = UsuarioBase(nome=usuario.nome, sobrenome=usuario.sobrenome,
                                email=usuario.email, senha=gerar_hash_senha(usuario.senha),
                                eh_admin=usuario.eh_admin)
    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()
            return novo_usuario
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='Já existe um usuário com esse E-mail cadastrado')

# GET Usuários
@router.get('/', response_model=List[UsuarioBase])
async def get_usuario(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioBase)
        result = await session.execute(query)
        usuarios = result.scalars().unique().all()
        return usuarios

# GET Usuário
@router.get('/{usuario_id}', response_model=UsuarioBase, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioBase).filter(UsuarioBase.id == usuario_id)
        result = await session.execute(query)
        usuario = result.scalar().unique().one_or_none()
        if usuario:
            return usuario
        else:
            raise HTTPException(detail='Usuário não encontrado...', status_code=status.HTTP_404_NOT_FOUND)

# PUT Usuário
@router.put('/{usuario_id}', response_model=UsuarioBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id: int, usuario: UsuarioBase, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioBase).filter(UsuarioBase.id == usuario_id)
        result = await session.execute(query)
        usuario_up = result.scalar().unique().one_or_none()
        if usuario_up:
            if usuario.nome:
                usuario_up.nome = usuario.nome
            if usuario.sobrenome:
                usuario_up.sobrenome = usuario.sobrenome
            if usuario.email:
                usuario_up.email = usuario.email
            if usuario.eh_admin:
                usuario_up.eh_admin = usuario.eh_admin
            if usuario.senha:
                usuario_up.senha = gerar_hash_senha(usuario.senha)
            await session.commit()
            return usuario_up
        else:
            raise HTTPException(detail='Usuário não encontrado...',
                                status_code=status.HTTP_404_NOT_FOUND)

# DELETE Usuário
@router.delete('/{usuario_id}', response_model=UsuarioBase, status_code=status.HTTP_200_OK)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioBase).filter(UsuarioBase.id == usuario_id)
        result = await session.execute(query)
        usuario_del = result.scalar().unique().one_or_none()
        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()
            return usuario_del
        else:
            raise HTTPException(detail='Usuário não encontrado!', status_code=status.HTTP_404_NOT_FOUND)

# POST Login
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Dados de usuário incorretos.')
    return JSONResponse(content={"access_token": criar_token_acesso(sub=usuario.id),
                                 "token_type": "bearer",}, status_code=status.HTTP_200_OK)
