from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from core.configs import settings
from api.v1.api import api_router

app = FastAPI(title='Fast API - Segurança e Autenticação')

app.include_router(api_router, prefix=settings.API_V1_STR)


# Manipulador de exceção para lidar com erros de validação de dados
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": "Erro de validação de dados", "details": exc.errors()},
    )


if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level='info', reload=True)
