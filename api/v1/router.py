
from fastapi import APIRouter
from api.v1.endpoints.productos import router as productos_router

router = APIRouter()

router.include_router(productos_router)
