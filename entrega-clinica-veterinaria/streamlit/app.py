import streamlit as st
import requests
import re  # Para validaciones adicionales

# URL del microservicio FastAPI
url_citas = "http://backend:8000/citas/"
url_facturas = "http://backend:8000/facturas/"
url_tratamientos = "http://backend:8000/tratamientos/"

# Título de la aplicación
st.title("Gestión de Clínica Veterinaria")

# Función para validar que un nombre contiene solo letras y espacios
def validar_nombre(nombre):
    return bool(re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+", nombre))

# ------------------------------
# Formulario para crear un tratamiento
st.header("Añadir tratamiento")
name = st.text_input("Nombre del tratamiento")
price = st.number_input("Precio del tratamiento", min_value=0.0)

if st.button("Añadir tratamiento"):
    # Validación del nombre
    if not validar_nombre(name):
        st.error("El nombre del tratamiento solo puede contener letras y espacios.")
    else:
        # Verificar si el tratamiento ya existe
        response = requests.get(url_tratamientos)
        if response.status_code == 200:
            treatments = response.json()
            if any(treatment['name'].lower() == name.lower() for treatment in treatments):
                st.warning("El tratamiento ya está añadido.")
            else:
                # Añadir el nuevo tratamiento
                response = requests.post(url_tratamientos, json={"name": name, "price": price})
                if response.status_code == 200:
                    st.success("Tratamiento añadido con éxito!")
                else:
                    st.error("Error al añadir tratamiento. Por favor, intenta de nuevo.")
        else:
            st.error("Error al verificar los tratamientos existentes.")

# Mostrar todos los tratamientos existentes
if st.button("Ver tratamientos"):
    response = requests.get(url_tratamientos)
    if response.status_code == 200:
        treatments = response.json()
        if treatments:
            for treatment in treatments:
                st.write(f"Tratamiento: {treatment['name']} - Precio: {treatment['price']}")
        else:
            st.info("No hay tratamientos registrados.")
    else:
        st.error("Error al obtener tratamientos.")

# ------------------------------
# Formulario para registrar una cita
st.header("Registrar cita")
animal_name = st.text_input("Nombre del animal")
owner_name = st.text_input("Nombre del dueño")
treatment = st.text_input("Tratamiento")
date = st.date_input("Fecha de la cita")

if st.button("Registrar cita"):
    if not validar_nombre(animal_name) or not validar_nombre(owner_name):
        st.error("El nombre del animal y del dueño solo pueden contener letras y espacios.")
    else:
        response = requests.post(url_citas, json={
            "animal_name": animal_name,
            "owner_name": owner_name,
            "treatment": treatment,
            "date": str(date)  # Convertir la fecha a string
        })

        if response.status_code == 200:
            st.success("Cita registrada exitosamente!")
        elif response.status_code == 404:
            st.error("El tratamiento especificado no existe. Por favor, verifica los datos.")
        else:
            st.error("Error al registrar la cita. Por favor, intenta de nuevo.")

# ------------------------------
# Formulario para generar una factura
st.header("Generar factura")
invoice_owner_name = st.text_input("Nombre del dueño para factura")
invoice_treatment = st.text_input("Tratamiento realizado")

invoice_price = st.number_input("Precio del tratamiento", min_value=0.0, key="invoice_price")
payment_method = st.selectbox("Método de pago", ["Transferencia", "Efectivo", "Tarjeta"], key="payment_method")

if st.button("Generar factura"):
    if not validar_nombre(invoice_owner_name):
        st.error("El nombre del dueño solo puede contener letras y espacios.")
    else:
        response = requests.post(url_facturas, json={
            "owner_name": invoice_owner_name,
            "treatment": invoice_treatment,
            "price": invoice_price,
            "payment_method": payment_method,
            "paid": True  # Asumimos que la factura está pagada
        })

        if response.status_code == 200:
            st.success("Factura generada exitosamente!")
        elif response.status_code == 404:
            st.error("El tratamiento especificado no existe o datos incorrectos. Por favor, verifica los datos.")
        else:
            st.error("Error al generar la factura. Por favor, intenta de nuevo.")
