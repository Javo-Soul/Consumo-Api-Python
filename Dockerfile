# Dockerfile
FROM python:3.11.5

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar y instalar las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar PostgreSQL client para poder interactuar con la base de datos
RUN apt-get update && apt-get install -y postgresql-client

# Copiar el resto de la aplicación
COPY . .

# Comando por defecto para ejecutar la aplicación
CMD ["python", "__main__.py"]


