import streamlit as st
import time

st.set_page_config(page_title='Ejemplito básico, de aquí al cielo', layout='wide',     page_icon="📈")
st.image('logo.jpg')

placeholder = st.empty()
with placeholder:
    #from PIL import Image
    #image = Image.open('mired.png')
    #placeholder.image(image, caption='MiRed semantic engine',use_column_width = 'always')
    for seconds in range(5):
        placeholder.write(f"⏳ {seconds} Cargando sistema")
        time.sleep(1)
placeholder.empty()


st.write("# Vamos a ello 👋")

st.sidebar.success("Selecciona una página. Eres libre de seleccionar.")

st.markdown(
    """
    Este ejemplo lo he adaptado de:
     1. La documentación oficial de [streamlit.io](https://streamlit.io), 
     2. De una estructura [multipágina](https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation)
     3. De un widget llamado [streamlit-calendar] () 
     4. Y, además, de  y de un proyecto de investigación
      
      
    Está basada en contenedores para para que entendáis cómo funciona docker y docker-compose y una aplicación basada
    en microservicios.
    Se divide en 3 páginas: 
    1. Un dashboard. No os fijéis en el contenido, porque en la página principal voy a volcar todo el contenido de un dataframe. Esto no debería hacerse así, sobretodo si el conjunto de datos es muy grande. 
    Es más, puedes gestionar datos desde `streamlit` (app monolítica), pero
    ya sabéis que una arquitectura basada en microservicios tiene ciertas ventajas sobre  una app monolítica.
    
    2. Un formulario: no es funcional
    3. Un calendario sobre el que se pueden mostrar e insertar / modificar datos (bien clickando, bien arrastrando un evento ya existente).
    
    Las páginas 2 y 3 no funcionan, a propósito. He dejado código sin completar, para que investiguéis cómo hacer una llamada post, qué tipo 
    de cabeceras podéis gestionar en una petición de HTTP, cuáles son los códigos de respuesta que os pueden dar, etc. Tenéis que empezar a investigar
    desde ya, siendo ya septiembre de 2024.
    
    Recordad: yo actuaré como cliente y, en casos muy concretos, como tecnólogo. Si me ofrecéis una funcionalidad, seguramente la quiera. Si os
    comprometéis y no cumplís, se os penalizará. Si la aplicación no funciona al final, el proyecto será un fracaso.
    
    A por ello 🫡🦮🦮!!
"""
)
