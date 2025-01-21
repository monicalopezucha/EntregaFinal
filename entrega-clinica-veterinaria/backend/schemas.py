from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time

class TratamientoBase(BaseModel):
    nombre: str
    precio: float

class TratamientoCreate(TratamientoBase):
    pass

class Tratamiento(TratamientoBase):
    id: int
    class Config:
        orm_mode = True

class ProductoBase(BaseModel):
    categoria: str
    marca: str
    precio: float
    cantidad: int

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
    class Config:
        orm_mode = True

# Esquemas de Citas
class CitaCreate(BaseModel):
    animal: str
    dueno: str
    tratamiento: str
    fecha: date

class Cita(BaseModel):
    id: int
    animal: str
    dueno: str
    tratamiento: str
    fecha: date

    class Config:
        orm_mode = True

class FacturaBase(BaseModel):
    cliente: str
    tratamientos: List[str]
    total: float
    metodo_pago: str
    estado_pago: str

class FacturaCreate(FacturaBase):
    pass

class Factura(FacturaBase):
    id: int
    class Config:
        orm_mode = True

