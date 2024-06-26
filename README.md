# ETL Project

Este proyecto es un script de ETL (Extract, Transform, Load) que obtiene datos de una API, los procesa y los almacena en una base de datos AWS Redshift.

## Estructura del Proyecto

- `__main__.py`: Punto de entrada del script. Llama a la API y procesa los datos.
- `modules/conexionSQL/conexionBD.py`: Módulo para manejar las conexiones a la base de datos PostgreSQL y Redshift.
- `modules/request/request.py`: Módulo para manejar las solicitudes a la API y el procesamiento de datos.
- `requirements.txt`: Lista de dependencias del proyecto.
- `.env`: Archivo que contiene las variables de entorno necesarias para las conexiones a la base de datos.

## Requisitos

- Python 3.x
- Las librerías listadas en `requirements.txt`
- Un archivo `.env` con las siguientes variables:
  - `REDSHIFT_HOST`
  - `REDSHIFT_USERNAME`
  - `REDSHIFT_PASSWORD`
  - `REDSHIFT_DBNAME`
  - `REDSHIFT_PORT`

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/tu_usuario/tu_repositorio.git
    cd tu_repositorio
    ```

2. Crea un entorno virtual y activa:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
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

El script realizará lo siguiente:

Llamará a la API de Jikan para obtener una lista de los mejores animes.
Procesará los datos y los guardará en un archivo CSV.
Cargará los datos desde el CSV a una base de datos AWS Redshift.
Logging
Los eventos y errores se registrarán en archivos de log:

conexionBD.log: Contiene los logs relacionados con las conexiones a la base de datos.
request.log: Contiene los logs relacionados con las solicitudes a la API y el procesamiento de datos.
Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que te gustaría hacer.

Licencia
Este proyecto está licenciado bajo la Licencia MIT.