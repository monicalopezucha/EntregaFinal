import pandas as pd
import streamlit as st
import plotly.express as px

st.title("Dashboard de la Clínica Veterinaria")

# Verificamos si existen facturas y tratamientos_data
if "facturas_registradas" not in st.session_state or len(st.session_state["facturas_registradas"]) == 0:
    st.info("No hay facturas registradas. Por favor, genere algunas facturas primero.")
    st.stop()

if "tratamientos_data" not in st.session_state or len(st.session_state["tratamientos_data"]) == 0:
    st.info("No hay tratamientos registrados en el sistema. Por favor, agregue tratamientos.")
    st.stop()

facturas = st.session_state["facturas_registradas"]
tratamientos_data = st.session_state["tratamientos_data"]

# Crear un DataFrame detallado por cada tratamiento de cada factura
# Cada fila representará un tratamiento realizado a un cliente en una factura
rows = []
for factura in facturas:
    cliente = factura["cliente"]
    lista_tratamientos = factura["tratamientos"]
    # Para cada tratamiento en la factura, añadimos una fila
    for t in lista_tratamientos:
        precio = tratamientos_data.get(t, 0.0)
        rows.append({
            "cliente": cliente,
            "tratamiento": t,
            "precio": precio,
            "estado_pago": factura["estado_pago"],
            "metodo_pago": factura["metodo_pago"],
            "total_factura": factura["total"]
        })

df_detalle = pd.DataFrame(rows)

if df_detalle.empty:
    st.info("No se encontraron tratamientos en las facturas.")
    st.stop()

# Ahora generamos las métricas a partir de df_detalle

# 1. Distribución de Tratamientos: cantidad de veces que aparece cada tratamiento
df_tratamientos = df_detalle.groupby("tratamiento").size().reset_index(name="cantidad")

# 2. Ingresos por Tratamiento: sumamos los precios unitarios de cada tratamiento
df_ingresos = df_detalle.groupby("tratamiento")["precio"].sum().reset_index(name="ingresos")

# 3. Clientes por Tratamiento: contamos clientes únicos por tratamiento
df_clientes = df_detalle.groupby("tratamiento")["cliente"].nunique().reset_index(name="clientes")

# 4. Ingresos mensuales (en el ejemplo original se mostraban datos simulados)
data_mensual = {
    "mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"],
    "ingresos": [10000, 12000, 15000, 13000, 11000, 16000]
}
df_mensual = pd.DataFrame(data_mensual)

# 5. Resumen numérico
total_tratamientos = df_tratamientos["cantidad"].sum()

# Ingresos totales
ingresos_totales = sum(f["total"] for f in facturas)

# Total de clientes
total_clientes = df_detalle["cliente"].nunique()

# Mostrar las gráficas y métricas

st.subheader("Distribución de Tratamientos y Clientes")
col1, col2 = st.columns(2)

with col1:
    fig1 = px.pie(df_tratamientos, names="tratamiento", values="cantidad", title="Distribución de Tratamientos")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(df_clientes, x="tratamiento", y="clientes", title="Clientes por Tratamiento", color="tratamiento", text="clientes")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Ingresos")
col3, col4 = st.columns(2)

with col3:
    fig3 = px.bar(df_ingresos, x="tratamiento", y="ingresos", title="Ingresos por Tratamiento", color="tratamiento", text="ingresos")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.line(df_mensual, x="mes", y="ingresos", title="Evolución Mensual de Ingresos (Simulada)", markers=True)
    st.plotly_chart(fig4, use_container_width=True)

st.subheader("Resumen Numérico")
col5, col6, col7 = st.columns(3)

with col5:
    st.metric("Total de Tratamientos", total_tratamientos)

with col6:
    st.metric("Ingresos Totales (€)", f"{ingresos_totales:,.2f}")

with col7:
    st.metric("Total de Clientes", total_clientes)
