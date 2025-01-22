import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime
import requests
import pandas as pd

st.title("Clínica Veterinaria - Gestión de Citas y Tratamientos 🐾")

# Configuración del backend
backend = "http://backend:8000"  # Cambia esta URL si es necesario

# Función para enviar datos al backend
def send_to_backend(endpoint, data):
    try:
        response = requests.post(f"{backend}/{endpoint}", json=data)
        if response.status_code == 200:
            return True, "Operación realizada con éxito"
        else:
            return False, f"Error: {response.status_code}"
    except Exception as e:
        return False, f"Error de conexión: {str(e)}"

# Función para recuperar citas desde el backend
def get_citas_from_backend():
    try:
        response = requests.get(f"{backend}/citas")  # Cambia el endpoint si es necesario
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"Error al obtener citas: {response.status_code}"
    except Exception as e:
        return None, f"Error de conexión: {str(e)}"

# Inicializar las citas en el estado de la aplicación
if "events" not in st.session_state:
    citas, error = get_citas_from_backend()
    if error:
        st.error(error)
        st.session_state["events"] = []
    else:
        st.session_state["events"] = [
            {"title": f"{cita['animal']} - {cita['tratamiento']}",
             "start": cita["fecha"],
             "end": cita["fecha"],
             "color": "#FF6C6C"}
            for cita in citas
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

# Gestionar nueva cita al seleccionar una fecha en el calendario
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
                data = {
                    "animal": nombre_animal,
                    "dueno": nombre_dueno,
                    "tratamiento": tratamiento,
                    "fecha": fecha
                }
                success, message = send_to_backend("citas", data)  # Endpoint para guardar cita
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

# Gestión de eventos existentes (modificación/cancelación)
if state.get("eventClick"):
    st.write(f"Modificar o cancelar cita: {state['eventClick']['event']['title']}")
    if st.button("Cancelar Cita"):
        event = state["eventClick"]["event"]
        st.session_state["events"] = [e for e in st.session_state["events"] if not (
            e["title"] == event["title"] and e["start"] == event["start"] and e["end"] == event["end"])]

        # Llamar al backend para cancelar la cita
        event_id = event.get('id')
        if event_id:
            response = requests.delete(f"{backend}/citas/{event_id}")
            if response.status_code == 200:
                st.success("Cita cancelada con éxito.")
            else:
                st.error("Error al cancelar la cita.")
        else:
            st.error("No se pudo identificar la cita para cancelar.")

# --- Gestión de Tratamientos ---
st.header("Gestión de Tratamientos 🩺")

# Inicializamos los tratamientos en session_state si no existen
if "tratamientos_data" not in st.session_state:
    st.session_state["tratamientos_data"] = {
        "Análisis: Sangre y Hormonales": 30.0,
        "Vacunación": 20.0,
        "Desparasitación": 15.0,
        "Revisión General": 25.0,
        "Revisión Cardiología": 40.0,
        "Revisión Cutánea": 35.0,
        "Ecografía": 50.0,
        "Cirugía: Castración": 100.0,
        "Limpieza Dental": 60.0
    }

st.write("Tratamientos disponibles (con precios):")

# Mostrar tabla de tratamientos a partir de session_state
df_tratamientos = pd.DataFrame({
    "Tratamiento": list(st.session_state["tratamientos_data"].keys()),
    "Precio (€)": list(st.session_state["tratamientos_data"].values())
})
st.table(df_tratamientos)

# Mostrar checkbox y formulario para añadir tratamientos
if st.checkbox("Añadir Nuevo Tratamiento"):
    with st.form("Nuevo Tratamiento"):
        nombre_tratamiento = st.text_input("Nombre del Tratamiento")
        precio = st.number_input("Precio (€)", min_value=0.0, step=0.1)
        submit_tratamiento = st.form_submit_button("Guardar Tratamiento")

        if submit_tratamiento:
            if nombre_tratamiento and precio >= 0:
                # Enviar datos al backend
                success, message = send_to_backend("tratamientos", {"nombre": nombre_tratamiento, "precio": precio})

                if success:
                    # Guardar en el estado
                    st.session_state["tratamientos_data"][nombre_tratamiento] = precio
                    st.success("Tratamiento añadido correctamente")
                else:
                    st.error(f"Error al guardar el tratamiento en el backend: {message}")
            else:
                st.error("Por favor, introduzca un nombre de tratamiento válido y un precio mayor o igual a 0.")

# Crear y mostrar la tabla actualizada si hay tratamientos
tratamientos_data = st.session_state["tratamientos_data"]
if tratamientos_data:
    df_tratamientos = pd.DataFrame({
        "Tratamiento": list(tratamientos_data.keys()),
        "Precio (€)": list(tratamientos_data.values())
    })
    st.table(df_tratamientos)
else:
    st.info("No hay tratamientos registrados aún.")

# Funcionalidad: Generación de Facturas
st.title("Gestión de Facturas 📄")

# Inicializar la lista de facturas registradas si no existe
if "facturas_registradas" not in st.session_state:
    st.session_state["facturas_registradas"] = []

# Función para mostrar las facturas registradas
def mostrar_facturas():
    if st.session_state["facturas_registradas"]:
        st.write("Listado de Facturas Registradas:")
        for factura in st.session_state["facturas_registradas"]:
            st.write(
                f"Cliente: {factura['cliente']}, "
                f"Tratamientos: {', '.join(factura['tratamientos'])}, "
                f"Total: €{factura['total']}, "
                f"Método de pago: {factura['metodo_pago']}, "
                f"Estado: {factura['estado_pago']}"
            )
    else:
        st.info("No hay facturas registradas.")

# Formulario para generar una nueva factura
st.subheader("Generar Nueva Factura")
cliente = st.text_input("Nombre del cliente")
tratamientos_realizados = st.multiselect(
    "Tratamientos realizados",
    list(tratamientos_data.keys())
)
forma_pago = st.selectbox("Método de pago", ["Efectivo", "Tarjeta", "Transferencia", "Otros"])
estado_pago = st.selectbox("Estado del pago", ["No Pagado", "Pagado"])
generar_factura = st.button("Generar Factura")

if generar_factura:
    if cliente and tratamientos_realizados:
        total = sum(tratamientos_data[t] for t in tratamientos_realizados if t in tratamientos_data)
        nueva_factura = {
            "cliente": cliente,
            "tratamientos": tratamientos_realizados,
            "total": total,
            "metodo_pago": forma_pago,
            "estado_pago": estado_pago
        }
        st.session_state["facturas_registradas"].append(nueva_factura)
        st.success(f"Factura generada y guardada con éxito para {cliente}. Total: €{total}")
        mostrar_facturas()
    else:
        st.error("Por favor, complete todos los campos.")

# Botón para ver todas las facturas
if st.button("Ver todas las facturas"):
    mostrar_facturas()
