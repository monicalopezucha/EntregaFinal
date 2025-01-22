import requests
from datetime import datetime
import re

# URL del microservicio FastAPI
url_citas = "http://backend:8000/citas/"
url_productos = "http://backend:8000/productos/"

st.title("Gestión de Veterinaria")

# Gestión de citas
st.header("Gestión de Citas")

# Crear el formulario para la creación de citas
with st.form("envio_citas"):
    nombre_animal = st.text_input("Nombre del animal")
    nombre_dueno = st.text_input("Nombre del dueño")
    tratamiento = st.selectbox("Tratamiento", ["Vacunación", "Revisión", "Ecografía", "Cirugía", "Otros"])
    fecha = st.date_input("Fecha de la cita", datetime.now().date())
    hora = st.time_input("Hora de la cita", datetime.now().time())
    submit_cita = st.form_submit_button(label="Registrar Cita")

# Validación de solo letras en nombre_animal y nombre_dueno
def es_nombre_valido(nombre):
    return bool(re.match("^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre))

if submit_cita:
    if not es_nombre_valido(nombre_animal):
        st.error("El nombre del animal solo debe contener letras.")
    elif not es_nombre_valido(nombre_dueno):
        st.error("El nombre del dueño solo debe contener letras.")
    else:
        # Crear el payload
        payload = {
            "animal": nombre_animal,
            "dueno": nombre_dueno,
            "tratamiento": tratamiento,
            "fecha": str(fecha),
        }

        # Enviar al backend
        response = requests.post(url_citas, json=payload)
        if response.status_code == 200:
            st.success("Cita registrada correctamente")
        elif response.status_code == 409:  # Si el animal ya tiene una cita
            st.warning("Ya existe una cita registrada para este animal.")
        else:
            st.error(f"Error al registrar la cita: {response.status_code}")

# Mostrar citas registradas
if st.button("Ver todas las citas"):
    response = requests.get(url_citas)
    if response.status_code == 200:
        citas = response.json()
        if citas:
            st.write("Citas registradas:")
            for cita in citas:
                st.write(
                    f"Animal: {cita['animal']}, Dueño: {cita['dueno']}, "
                    f"Tratamiento: {cita['tratamiento']}, Fecha: {cita['fecha']}"
                )
        else:
            st.info("No hay citas registradas.")
    else:
        st.error(f"Error al obtener las citas: {response.status_code}")

# Gestión de productos
st.header("Gestión de Productos")

# Menú de acciones para productos
accion_producto = st.selectbox("Selecciona una acción", [
    "Alta de productos",
    "Baja de productos",
    "Modificación de productos",
    "Búsqueda de productos",
    "Venta de productos"
])

if accion_producto == "Alta de productos":
    st.subheader("Registrar Nuevo Producto")
    categoria = st.selectbox("Selecciona la categoría", [
        "Vitaminas",
        "Cremas analgésicas",
        "Desparasitador",
        "Productos de belleza"
    ])
    marca = st.text_input("Marca del producto")
    precio = st.number_input("Precio del producto", min_value=0.1, step=0.1)  # Evitar precio 0
    cantidad = st.number_input("Cantidad del producto", min_value=1, step=1)
    if st.button("Registrar producto"):
        # Verificar si ya existe un producto con la misma marca
        response = requests.get(f"{url_productos}?search={marca}")
        if response.status_code == 200:
            productos_existentes = response.json()
            if productos_existentes:
                st.warning(f"El producto '{marca}' ya está registrado.")
            else:
                payload = {
                    "categoria": categoria,
                    "marca": marca,
                    "precio": precio,
                    "cantidad": cantidad
                }
                response = requests.post(url_productos, json=payload)
                if response.status_code == 200:
                    st.success(f"Producto '{marca}' registrado correctamente.")
                else:
                    st.error(f"Error al registrar el producto: {response.status_code}")
        else:
            st.error(f"Error al verificar el producto: {response.status_code}")

elif accion_producto == "Baja de productos":
    st.subheader("Eliminar Producto")
    producto_a_eliminar = st.text_input("Introduce la marca del producto a eliminar")
    if st.button("Eliminar producto"):
        url_a_eliminar = f"{url_productos.rstrip('/')}/{producto_a_eliminar}"
        response = requests.delete(url_a_eliminar)
        if response.status_code == 200:
            st.success(f"Producto '{producto_a_eliminar}' eliminado correctamente.")
        elif response.status_code == 404:
            st.warning(f"El producto '{producto_a_eliminar}' no se encuentra registrado.")
        else:
            st.error(f"Error al eliminar el producto: {response.status_code}")

elif accion_producto == "Modificación de productos":
    st.subheader("Modificar Producto")
    producto_a_modificar = st.text_input("Introduce la marca del producto a modificar")
    nuevo_precio = st.number_input("Nuevo precio", min_value=0.1, step=0.1)

    if st.button("Modificar producto"):
        if producto_a_modificar and nuevo_precio > 0:
            url_a_modificar = f"{url_productos.rstrip('/')}/{producto_a_modificar}"
            params = {"precio": nuevo_precio}
            response = requests.put(url_a_modificar, params=params)
            if response.status_code == 200:
                st.success(f"Producto '{producto_a_modificar}' modificado correctamente.")
            elif response.status_code == 422:
                error_msg = response.json().get("detail", "Error desconocido.")
                st.error(f"No se pudo modificar el producto: {error_msg}")
            else:
                st.error(f"Error al modificar el producto: Código {response.status_code}")
        else:
            st.error("Debes ingresar el nombre del producto y un precio válido.")

elif accion_producto == "Venta de productos":
    st.subheader("Venta de Producto")
    response = requests.get(url_productos)
    if response.status_code == 200:
        productos = response.json()
        productos_disponibles = [p for p in productos if p['cantidad'] > 0]
        if productos_disponibles:
            producto_venta = st.selectbox("Selecciona el producto a vender", [p['marca'] for p in productos_disponibles])
            cantidad_venta = st.number_input("Cantidad a vender", min_value=1, step=1)
            if st.button("Realizar venta"):
                if cantidad_venta > 0:
                    url_venta = f"{url_productos.rstrip('/')}/{producto_venta}/venta?cantidad={int(cantidad_venta)}"
                    response = requests.post(url_venta)
                    if response.status_code == 200:
                        st.success(f"Venta de {cantidad_venta} unidades del producto '{producto_venta}' realizada correctamente.")
                    else:
                        st.error(f"Error al realizar la venta: {response.status_code}, Detalles: {response.text}")
                else:
                    st.error("La cantidad a vender debe ser mayor que cero.")
        else:
            st.info("No hay productos disponibles para la venta.")
    else:
        st.error(f"Error al obtener los productos: {response.status_code}")

elif accion_producto == "Búsqueda de productos":
    st.subheader("Buscar Producto")
    criterio_busqueda = st.text_input("Introduce el nombre o parte del nombre del producto")
    if criterio_busqueda:
        response = requests.get(f"{url_productos}?search={criterio_busqueda}")
        if response.status_code == 200:
            resultados = response.json()
            if resultados:
                st.write("Resultados de la búsqueda:")
                for producto in resultados:
                    st.write(
                        f"Producto: {producto['marca']}, Categoría: {producto['categoria']}, "
                        f"Precio: {producto['precio']}, Stock: {producto['cantidad']}"
                    )
            else:
                st.info("No se encontraron productos que coincidan con la búsqueda.")
        else:
            st.error(f"Error al buscar productos: {response.status_code}")
