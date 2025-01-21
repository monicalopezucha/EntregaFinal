from sqlalchemy.orm import Session
from models import Cita, Factura, Producto, Tratamiento
from schemas import CitaCreate, FacturaCreate, ProductoCreate, TratamientoCreate
from datetime import date, datetime

# Crear un tratamiento
def create_tratamiento(db: Session, tratamiento: TratamientoCreate):
    db_tratamiento = Tratamiento(nombre=tratamiento.nombre, precio=tratamiento.precio, tipo=tratamiento.tipo)
    db.add(db_tratamiento)
    db.commit()
    db.refresh(db_tratamiento)
    return db_tratamiento

# Crear un producto
def create_producto(db: Session, producto: ProductoCreate):
    db_producto = Producto(nombre=producto.nombre, categoria=producto.categoria, marca=producto.marca,
                           precio=producto.precio, stock=producto.stock)
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

# Crear una cita
def create_cita(db: Session, cita: CitaCreate):
    db_cita = Cita(nombre_animal=cita.nombre_animal,
                   nombre_dueno=cita.nombre_dueno,
                   fecha=cita.fecha,
                   tratamiento_id=cita.tratamiento_id)
    db.add(db_cita)
    db.commit()
    db.refresh(db_cita)
    return db_cita

# Crear una factura
def create_factura(db: Session, factura: FacturaCreate):
    db_factura = Factura(fecha_emision=factura.fecha_emision, total=factura.total, metodo_pago=factura.metodo_pago)
    db.add(db_factura)
    db.commit()
    db.refresh(db_factura)
    return db_factura

# Actualizar un tratamiento
def update_tratamiento(db: Session, tratamiento_id: int, tratamiento: TratamientoCreate):
    db_tratamiento = db.query(Tratamiento).filter(Tratamiento.id == tratamiento_id).first()
    if db_tratamiento:
        db_tratamiento.nombre = tratamiento.nombre
        db_tratamiento.precio = tratamiento.precio
        db_tratamiento.tipo = tratamiento.tipo
        db.commit()
        db.refresh(db_tratamiento)
        return db_tratamiento
    return None

# Eliminar un tratamiento
def delete_tratamiento(db: Session, tratamiento_id: int):
    db_tratamiento = db.query(Tratamiento).filter(Tratamiento.id == tratamiento_id).first()
    if db_tratamiento:
        db.delete(db_tratamiento)
        db.commit()
        return db_tratamiento
    return None

# Actualizar cita
def update_cita(db: Session, cita_id: int, nueva_fecha: date, tratamiento_id: int):
    db_cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if db_cita:
        db_cita.fecha = nueva_fecha
        db_cita.tratamiento_id = tratamiento_id
        db.commit()
        db.refresh(db_cita)
        return db_cita
    return None

# Cancelar cita
def cancel_cita(db: Session, cita_id: int):
    db_cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if db_cita:
        db.delete(db_cita)
        db.commit()
        return db_cita
    return None

# Generar factura
def generate_factura(db: Session, cita_id: int, metodo_pago: str):
    db_cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if db_cita:
        total = db_cita.tratamiento.precio  # Podrías incluir más cálculos aquí si hay más tratamientos.
        factura = Factura(cita_id=cita_id, fecha_emision=date.today(), total=total, metodo_pago=metodo_pago)
        db.add(factura)
        db.commit()
        db.refresh(factura)
        return factura
    return None

# Función para buscar productos por marca
def search_productos(db: Session, search: str):
    return db.query(Producto).filter(Producto.marca.contains(search)).all()

# Función para actualizar el stock de un producto tras una venta
def sell_producto(db: Session, marca: str, cantidad: int):
    db_producto = db.query(Producto).filter(Producto.marca == marca).first()
    if not db_producto:
        return None, "Producto no encontrado"
    if db_producto.stock < cantidad:
        return None, "Stock insuficiente"
    db_producto.stock -= cantidad
    db.commit()
    db.refresh(db_producto)
    return db_producto, None

# Función para obtener todos los tratamientos
def get_tratamientos(db: Session):
    return db.query(Tratamiento).all()

# Función para crear una cita con hora
def create_cita_with_time(db: Session, cita: CitaCreate, hora: str):
    fecha_hora = datetime.combine(cita.fecha, datetime.strptime(hora, "%H:%M:%S").time())
    db_cita = Cita(
        nombre_animal=cita.nombre_animal,
        nombre_dueno=cita.nombre_dueno,
        fecha=fecha_hora,
        tratamiento_id=cita.tratamiento_id
    )
    db.add(db_cita)
    db.commit()
    db.refresh(db_cita)
    return db_cita

# Función para obtener citas con formato detallado
def get_citas_with_details(db: Session):
    citas = db.query(Cita).all()
    result = []
    for cita in citas:
        tratamiento = db.query(Tratamiento).filter(Tratamiento.id == cita.tratamiento_id).first()
        result.append({
            "id": cita.id,
            "nombre_animal": cita.nombre_animal,
            "nombre_dueno": cita.nombre_dueno,
            "fecha": cita.fecha.strftime("%Y-%m-%d"),
            "hora": cita.fecha.strftime("%H:%M:%S"),
            "tratamiento": tratamiento.nombre if tratamiento else "Desconocido"
        })
    return result
