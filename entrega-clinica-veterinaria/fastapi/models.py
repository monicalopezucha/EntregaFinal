from enum import Enum
from datetime import datetime
from pydantic import BaseModel

class Treatment(BaseModel):
    id: int
    name: str
    price: float

class Appointment(BaseModel):
    animal_name: str  # Nombre del animal
    owner_name: str  # Nombre del dueño
    treatment: str  # Tratamiento que se realizará
    date: datetime  # Fecha y hora de la cita
    completed: bool = False  # Indica si la cita está completada o no

class PaymentMethod(str, Enum):
    transfer = "Transferencia"
    cash = "Efectivo"
    card = "Tarjeta"

# Modelo de la factura
class Invoice(BaseModel):
    owner_name: str  # Nombre del dueño
    treatment: str  # Tratamiento realizado
    price: float  # Precio del tratamiento
    payment_method: PaymentMethod  # Método de pago
    paid: bool  # Indica si la factura ha sido pagada

