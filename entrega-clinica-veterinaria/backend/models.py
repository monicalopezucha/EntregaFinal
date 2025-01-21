from sqlalchemy import Column, Integer, String, Float, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel
from datetime import date

class Tratamiento(Base):
    __tablename__ = "tratamientos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    precio = Column(Float)

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    categoria = Column(String)
    marca = Column(String, unique=True)
    precio = Column(Float)
    cantidad = Column(Integer)

class Cita(Base):
    __tablename__ = "citas"
    id = Column(Integer, primary_key=True, index=True)
    animal = Column(String)
    dueno = Column(String)
    tratamiento = Column(String)
    fecha = Column(Date)

class Factura(Base):
    __tablename__ = "facturas"
    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String)
    tratamientos = Column(String)  # Lista de tratamientos como cadena JSON
    total = Column(Float)
    metodo_pago = Column(String)
    estado_pago = Column(String)

class FormData(BaseModel):
    nombre_animal: str
    nombre_dueno: str
    tratamiento: str
    fecha: str


