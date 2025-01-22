from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Cita, Factura, Producto, Tratamiento, FormData
from database import get_db
from schemas import CitaCreate, FacturaCreate, ProductoCreate, TratamientoCreate

router_citas = APIRouter()
router_facturas = APIRouter()
router_productos = APIRouter()
router_tratamientos = APIRouter()


# Rutas de citas
@router_citas.get("/")
def get_citas(db: Session = Depends(get_db)):
    return db.query(Cita).all()

@router_citas.post("/")
def create_cita(cita: CitaCreate, db: Session = Depends(get_db)):
    nueva_cita = Cita(**cita.dict())
    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)
    return nueva_cita

# Rutas de facturas
@router_facturas.get("/")
def read_facturas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Factura).offset(skip).limit(limit).all()

@router_facturas.post("/")
def create_factura(factura: FacturaCreate, db: Session = Depends(get_db)):
    db_factura = Factura(**factura.dict())
    db.add(db_factura)
    db.commit()
    db.refresh(db_factura)
    return db_factura

# Rutas de productos
@router_productos.get("/")
def read_productos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Producto).offset(skip).limit(limit).all()

@router_productos.post("/")
def create_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router_productos.delete("/{marca}")
def delete_producto(marca: str, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.marca == marca).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()
    return {"detail": "Producto eliminado correctamente"}

@router_productos.put("/{marca}")
def update_producto(marca: str, precio: float, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.marca == marca).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto.precio = precio
    db.commit()
    db.refresh(producto)
    return producto

@router_productos.post("/{marca}/venta")
def sell_producto(marca: str, cantidad: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.marca == marca).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if producto.cantidad < cantidad:
        raise HTTPException(status_code=400, detail="Stock insuficiente")
    producto.cantidad -= cantidad
    db.commit()
    db.refresh(producto)
    return producto

# Rutas de tratamientos
@router_tratamientos.get("/")
def read_tratamientos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Tratamiento).offset(skip).limit(limit).all()

@router_tratamientos.post("/")
def create_tratamiento(tratamiento: TratamientoCreate, db: Session = Depends(get_db)):
    db_tratamiento = Tratamiento(**tratamiento.dict())
    db.add(db_tratamiento)
    db.commit()
    db.refresh(db_tratamiento)
    return db_tratamiento

# Rutas para buscar productos
@router_productos.get("/search")
def search_productos(search: str, db: Session = Depends(get_db)):
    productos = search_productos(db, search)
    if not productos:
        raise HTTPException(status_code=404, detail="No se encontraron productos.")
    return productos

# Rutas para obtener tratamientos
@router_tratamientos.get("/list")
def get_tratamientos(db: Session = Depends(get_db)):
    return get_tratamientos(db)

# Rutas para crear citas con hora
@router_citas.post("/with_time")
def create_cita_with_time(cita: CitaCreate, hora: str, db: Session = Depends(get_db)):
    return create_cita_with_time(db, cita, hora)

# Rutas para obtener citas detalladas
@router_citas.get("/details")
def get_citas_with_details(db: Session = Depends(get_db)):
    return get_citas_with_details(db)


