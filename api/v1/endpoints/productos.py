from fastapi import APIRouter, HTTPException
from pymongo.errors import PyMongoError

from schemas.catalogo import CatalogoCreate
from core.database import productos_collection

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post("/")
async def registrar_producto(producto: CatalogoCreate):
    try:
        nuevo_producto = producto.model_dump()

        resultado = await productos_collection.insert_one(nuevo_producto)

        nuevo_producto["_id"] = str(resultado.inserted_id)

        return {
            "mensaje": "Producto registrado correctamente",
            "id": str(resultado.inserted_id),
            "producto": nuevo_producto
        }

    except PyMongoError as error:
        print(f"Error de MongoDB: {error}")
        raise HTTPException(
            status_code=500,
            detail="Error al registrar el producto en la base de datos"
        )