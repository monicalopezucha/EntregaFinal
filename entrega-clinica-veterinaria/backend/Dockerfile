FROM python:3.11-slim

# Crea y establece el directorio de trabajo
WORKDIR /backend

# Copia los archivos de requerimientos e instala las dependencias
COPY requirements.txt /backend
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código fuente al contenedor
COPY . /backend

EXPOSE 8000

# Comando para ejecutar el servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
