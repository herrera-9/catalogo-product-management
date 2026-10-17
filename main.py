from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.database import connect_to_mongo, close_mongo_connection
from api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manejo del ciclo de vida de la aplicación.
    Conexión y desconexión a MongoDB.
    """
    try:
        await connect_to_mongo()
    except Exception as e:
        print(f">> Advertencia: No se pudo conectar a MongoDB al iniciar: {e}")
    
    yield

    try:
        await close_mongo_connection()
    except Exception as e:
        print(f">> Advertencia al cerrar conexión de MongoDB: {e}")


# Instancia principal de FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API REST para gestión de tareas construida con FastAPI y MongoDB.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Configuración de Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión del enrutador v1
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["root"])
async def root():
    """
    Endpoint de bienvenida e información básica de la API.
    """
    return {
        "title": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)
