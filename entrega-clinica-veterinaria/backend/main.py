from fastapi import FastAPI, Depends, HTTPException
from database import Base, engine, get_db, SessionLocal
from routes import router_citas, router_facturas, router_productos, router_tratamientos

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Inicializar FastAPI
app = FastAPI(debug=True)

# Incluir rutas
app.include_router(router_citas, prefix="/citas", tags=["Citas"])
app.include_router(router_facturas, prefix="/facturas", tags=["facturas"])
app.include_router(router_productos, prefix="/productos", tags=["Productos"])
app.include_router(router_tratamientos, prefix="/tratamientos", tags=["Tratamientos"])


@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}
