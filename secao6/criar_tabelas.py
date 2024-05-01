from core.configs import settings
from core.database import engine

async def drop_all_tables() -> None:
    """
    Função assíncrona para excluir todas as tabelas do banco de dados.
    """
    print('Excluindo todas as tabelas do banco de dados...')
    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
    print('Todas as tabelas excluídas com sucesso.')

async def create_all_tables() -> None:
    """
    Função assíncrona para criar todas as tabelas no banco de dados.
    """
    print('Criando todas as tabelas no banco de dados...')
    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
    print('Todas as tabelas criadas com sucesso.')

async def create_tables() -> None:
    """
    Função assíncrona para criar e excluir todas as tabelas no banco de dados.
    """
    await drop_all_tables()
    await create_all_tables()

if __name__ == '__main__':
    import asyncio
    
    asyncio.run(create_tables())
