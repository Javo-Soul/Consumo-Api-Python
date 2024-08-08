# Consumo-Api-Python

## Descripción
Este proyecto es un script de ETL (Extract, Transform, Load) que obtiene datos de una API, los procesa y los almacena en una base de datos AWS Redshift.

## Iniciar el Proyecto

### Iniciar con Docker
```bash
docker compose up airflow-init
```
```bash
docker compose up --build
```

### Ingreso a Airflow web
1. En el navegador, ve a [http://localhost:8081](http://localhost:8081).
2. Inicia sesión con el usuario `airflow` y la contraseña `airflow`.

## Estructura del Proyecto

- `.dockerignore`: Archivos y directorios ignorados por Docker.
- `.gitignore`: Archivos y directorios ignorados por Git.
- `Dockerfile`: Instrucciones para construir la imagen Docker.
- `docker-compose.yml`: Configuración de servicios Docker.
- `requirements.txt`: Dependencias de Python.
- `start.sh`: Script para iniciar la aplicación.
- `init_db.sql`: Script SQL para inicializar la base de datos.
- `__main__.py`: Archivo principal de la aplicación.
- `config/`: Archivos de configuración.
- `logs/`: se guardan los Logs de las ejecuciones de airflow
- `dags/`: DAGs para Airflow.
- `modules/`: Módulos de Python.
- `venv/`: Entorno virtual de Python.


## Requisitos

- Python 3.11.5
- Las librerías listadas en `requirements.txt`
- Un archivo `.env` con las siguientes variables:

- POSTGRES_HOST=localhost
- POSTGRES_USER=postgres
- POSTGRES_PASSWORD=passxxx.
- POSTGRES_PORT=5432
- POSTGRES_DB=postgres
- AIRFLOW_UID=1000
- EMAIL_SUBJECT=xxxxxxx@gmail.com
- EMAIL_PASSWORD=xxxxxxxx

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/tu_usuario/tu_repositorio.git
    cd tu_repositorio
    ```

2. Crea un entorno virtual y actívalo:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scriptsctivate`
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Configura las variables de entorno en un archivo `.env` en la raíz del proyecto:
    ```env
    REDSHIFT_HOST=tu_redshift_host
    REDSHIFT_USERNAME=tu_usuario
    REDSHIFT_PASSWORD=tu_contraseña
    REDSHIFT_DBNAME=tu_base_de_datos
    REDSHIFT_PORT=tu_puerto
    ```

## Uso

Para ejecutar el script, usa el siguiente comando:
```bash
python __main__.py
```

El script realizará lo siguiente:
1. Llamará a la API de Jikan para obtener una lista de los mejores animes.
2. Procesará los datos y los guardará en un archivo CSV.
3. Cargará los datos desde el CSV a una base de datos AWS Redshift.

## Logging

Los eventos y errores se registrarán en archivos de log:
- `conexionBD.log`: Contiene los logs relacionados con las conexiones a la base de datos.
- `request.log`: Contiene los logs relacionados con las solicitudes a la API y el procesamiento de datos.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que te gustaría hacer.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.
