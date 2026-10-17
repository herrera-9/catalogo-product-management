
from pydantic import BaseModel, Field


class CatalogoCreate(BaseModel):
    nombre: str = Field(..., min_length=1)
    descripcion: str = Field(..., min_length=1)
    precio: float = Field(..., gt=0)
    categoria: str = Field(..., min_length=1)
    marca: str = Field(..., min_length=1)
    stock: int = Field(..., ge=0)
