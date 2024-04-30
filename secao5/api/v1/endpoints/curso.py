
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.curso_model import CursoModel
from core.deps import get_session

# Baypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # Correção da digitação
Select.inherit_cache = True  # Correção da digitação
# Fim do Bypass

router = APIRouter()

# POST CURSO
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CursoModel)
async def post_curso(curso: CursoModel, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)
   
    db.add(novo_curso)
    await db.commit()
    
    return novo_curso

# GET CURSOS
@router.get('/', response_model=List[CursoModel])
async def get_cursos(db: AsyncSession = Depends(get_session)):  # Renomeando a função
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()  # Corrigindo o método de obtenção dos resultados

        return cursos

# GET CURSO POR ID
@router.get('/{curso_id}', response_model=CursoModel, status_code=status.HTTP_200_OK)
async def get_curso_id(curso_id: int, db: AsyncSession = Depends(get_session)):  # Renomeando a função
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso = result.scalars().first()  # Corrigindo o método de obtenção do resultado

        if curso:
            return curso 
        else:
            raise HTTPException(detail='Curso não encontrado', 
                                status_code=status.HTTP_404_NOT_FOUND)
        
        
# PUT CURSO
@router.put('/{curso_id}', status_code=status.HTTP_202_ACCEPTED, response_model=CursoModel)
async def put_curso(curso_id: int, curso: CursoModel, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_up = result.scalars().first()  # Corrigindo o método de obtenção do resultado
        
        if curso_up:
            curso_up.titulo = curso.titulo
            curso_up.aulas = curso.aulas
            curso_up.horas = curso.horas
            
            await session.commit()
            
            return curso_up
        else:
            raise HTTPException(detail='Curso não encontrado.', 
                                status_code=status.HTTP_404_NOT_FOUND)
            
# CURSO DELETE
@router.delete('/{curso_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_del = result.scalars().first()  # Corrigindo o método de obtenção do resultado
        
        if curso_del:
            await session.delete(curso_del)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Curso não encontrado.', 
                                status_code=status.HTTP_404_NOT_FOUND)
