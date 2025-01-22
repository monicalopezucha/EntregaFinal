import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime
import requests
import pandas as pd

st.title("Clínica Veterinaria - Gestión de Citas y Tratamientos 🐾")

# Configuración del backend
backend_url = "http://backend:8000"

# Función para enviar datos al backend
def send_to_backend(endpoint, data):
    try:
        response = requests.post(f"{backend_url}/{endpoint}", json=data)
        if response.status_code == 200:
            return True, "Operación realizada con éxito"
        else:
            return False, f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return False, f"Error de conexión: {str(e)}"

# Función para recuperar datos desde el backend
def get_from_backend(endpoint):
    try:
        response = requests.get(f"{backend_url}/{endpoint}")
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return None, f"Error de conexión: {str(e)}"

# Inicializar citas en el estado de la aplicación
if "events" not in st.session_state:
    citas, error = get_from_backend("citas")
    if error:
        st.error(error)
        st.session_state["events"] = []
    else:
        st.session_state["events"] = [
            {"title": f"{cita['animal']} - {cita['tratamiento']}",
             "start": cita["fecha"],
             "end": cita["fecha"],
             "color": "#FF6C6C",
             "id": cita["id"]} for cita in citas
        ]

# Opciones de configuración del calendario
calendar_options = {
    "editable": "true",
    "navLinks": "true",
    "initialDate": datetime.now().strftime("%Y-%m-%d"),
    "initialView": "dayGridMonth",
    "selectable": "true",
}

# Mostrar el calendario interactivo
state = calendar(
    events=st.session_state["events"],
    options=calendar_options,
    custom_css=""".fc-event-title { font-weight: bold; } .fc-toolbar-title { font-size: 1.5rem; }""",
    key='calendar'
)

# Añadir nueva cita
if state.get("select"):
    with st.form("Nueva Cita"):
        nombre_animal = st.text_input("Nombre del animal")
        nombre_dueno = st.text_input("Nombre del dueño")
        tratamiento = st.selectbox("Tratamiento", ["Análisis", "Vacunación", "Revisión General", "Cirugía"])
        fecha = state["select"]["start"][:10]
        st.write(f"Fecha seleccionada: {fecha}")
        submit = st.form_submit_button("Guardar Cita")

        if submit:
            if not nombre_animal or not nombre_dueno:
                st.error("Por favor, complete todos los campos.")
            else:
                nueva_cita = {
                    "animal": nombre_animal,
                    "dueno": nombre_dueno,
                    "tratamiento": tratamiento,
                    "fecha": fecha
                }
                success, message = send_to_backend("citas", nueva_cita)
                if success:
                    st.success(message)
                    st.session_state["events"].append({
                        "title": f"{nombre_animal} - {tratamiento}",
                        "start": fecha,
                        "end": fecha,
                        "color": "#FF6C6C"
                    })
                else:
                    st.error(message)

# Modificar o cancelar cita existente
if state.get("eventClick"):
    st.write(f"Modificar o cancelar cita: {state['eventClick']['event']['title']}")
    event_id = state["eventClick"]["event"]["id"]

    if st.button("Cancelar Cita"):
        response = requests.delete(f"{backend_url}/citas/{event_id}")
        if response.status_code == 200:
            st.success("Cita cancelada con éxito.")
            st.session_state["events"] = [e for e in st.session_state["events"] if e["id"] != event_id]
        else:
            st.error(f"Error al cancelar la cita: {response.text}")

# --- Gestión de Tratamientos ---
st.header("Gestión de Tratamientos 🩺")

# Inicializar tratamientos en el estado
if "tratamientos_data" not in st.session_state:
    tratamientos, error = get_from_backend("tratamientos")
    if error:
        st.error(error)
        st.session_state["tratamientos_data"] = {}
    else:
        st.session_state["tratamientos_data"] = {t["nombre"]: t["precio"] for t in tratamientos}

tratamientos_data = st.session_state["tratamientos_data"]
st.write("Tratamientos disponibles (con precios):")
df_tratamientos = pd.DataFrame({
    "Tratamiento": list(tratamientos_data.keys()),
    "Precio (€)": list(tratamientos_data.values())
})
st.table(df_tratamientos)

if st.checkbox("Añadir Nuevo Tratamiento"):
    with st.form("Nuevo Tratamiento"):
        nombre_tratamiento = st.text_input("Nombre del Tratamiento")
        precio = st.number_input("Precio (€)", min_value=0.0, step=0.1)
        submit_tratamiento = st.form_submit_button("Guardar Tratamiento")

        if submit_tratamiento:
            if nombre_tratamiento and precio >= 0:
                nuevo_tratamiento = {"nombre": nombre_tratamiento, "precio": precio}
                success, message = send_to_backend("tratamientos", nuevo_tratamiento)
                if success:
                    st.session_state["tratamientos_data"][nombre_tratamiento] = precio
                    st.success("Tratamiento añadido correctamente.")
                else:
                    st.error(f"Error al guardar el tratamiento: {message}")
            else:
                st.error("Por favor, complete todos los campos.")

# --- Generación de Facturas ---
st.header("Gestión de Facturas 📄")

def mostrar_facturas():
    facturas, error = get_from_backend("facturas")
    if error:
        st.error(error)
    elif facturas:
        st.write("Listado de Facturas:")
        for factura in facturas:
            st.write(
                f"Fecha: {factura['fecha_emision']}, Cliente: {factura['cliente']}, "
                f"Total: €{factura['total']}, Método de pago: {factura['metodo_pago']}"
            )
    else:
        st.info("No hay facturas registradas.")

st.subheader("Generar Nueva Factura")
cliente = st.text_input("Nombre del cliente")
tratamientos_realizados = st.multiselect("Tratamientos realizados", list(tratamientos_data.keys()))
forma_pago = st.selectbox("Método de pago", ["Efectivo", "Tarjeta", "Transferencia", "Otros"])
estado_pago = st.selectbox("Estado del pago", ["No Pagado", "Pagado"])
if st.button("Generar Factura"):
    if cliente and tratamientos_realizados:
        total = sum(tratamientos_data[t] for t in tratamientos_realizados)
        nueva_factura = {
            "cliente": cliente,
            "tratamientos": tratamientos_realizados,
            "total": total,
            "metodo_pago": forma_pago,
            "estado_pago": estado_pago
        }
        success, message = send_to_backend("facturas", nueva_factura)
        if success:
            st.success(f"Factura generada correctamente para {cliente}. Total: €{total}")
        else:
            st.error(f"Error al guardar la factura: {message}")
    else:
        st.error("Complete todos los campos.")

if st.button("Ver Facturas"):
    mostrar_facturas()
