from fastapi import FastAPI, HTTPException
from typing import List
from models import Treatment, Appointment, Invoice, PaymentMethod  # Asegúrate de importar correctamente los modelos

app = FastAPI()

# Lista para almacenar los tratamientos
treatments = []

# Lista para almacenar las citas
appointments = []

# Lista para almacenar las facturas generadas
invoices = []


# Rutas para tratamientos
@app.post("/treatments/")
def create_treatment(treatment: Treatment):
    # Validar si ya existe un tratamiento con el mismo nombre
    if any(t.name == treatment.name for t in treatments):
        raise HTTPException(status_code=400, detail="Treatment already exists")

    treatments.append(treatment)
    return {"message": "Treatment added successfully", "treatment": treatment}


@app.get("/treatments/", response_model=List[Treatment])
def get_treatments():
    return treatments


@app.delete("/treatments/{treatment_id}")
def delete_treatment(treatment_id: int):
    treatment = next((t for t in treatments if t.id == treatment_id), None)
    if treatment:
        treatments.remove(treatment)
        return {"message": "Treatment deleted successfully"}
    raise HTTPException(status_code=404, detail="Treatment not found")


# Rutas para citas
@app.post("/appointments/")
def create_appointment(appointment: Appointment):
    appointments.append(appointment)
    return {"message": "Appointment created successfully", "appointment": appointment}


@app.get("/appointments/", response_model=List[Appointment])
def get_appointments():
    return appointments


@app.put("/appointments/{appointment_id}")
def update_appointment(appointment_id: int, appointment: Appointment):
    for idx, app in enumerate(appointments):
        if app.id == appointment_id:
            appointments[idx] = appointment
            return {"message": "Appointment updated successfully", "appointment": appointment}
    raise HTTPException(status_code=404, detail="Appointment not found")


@app.delete("/appointments/{appointment_id}")
def cancel_appointment(appointment_id: int):
    for idx, app in enumerate(appointments):
        if app.id == appointment_id:
            canceled_appointment = appointments.pop(idx)
            return {"message": f"Appointment for {canceled_appointment.animal_name} canceled"}
    raise HTTPException(status_code=404, detail="Appointment not found")


# Ruta para generar la factura
@app.post("/invoices/")
def generate_invoice(appointment_id: int, payment_method: PaymentMethod, paid: bool):
    # Buscar la cita correspondiente por ID
    appointment = next((app for app in appointments if app.id == appointment_id), None)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # Crear la factura
    price = 100  # Precio del tratamiento (esto puede ser calculado o definido de otra manera)
    invoice = Invoice(
        owner_name=appointment.owner_name,
        treatment=appointment.treatment,
        price=price,
        payment_method=payment_method,
        paid=paid
    )

    # Añadir la factura a la lista
    invoices.append(invoice)

    # Marcar la cita como completada
    appointment.completed = True

    return {"message": "Invoice generated", "invoice": invoice}
