import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import logging

# Configuración del logging
logging.basicConfig(
    filename='conexionBD.log',  # Nombre del archivo de log
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

load_dotenv()

class ConexionesSQL:
    @staticmethod
    def conexion_postgres():
        try:
            host = os.getenv('REDSHIFT_HOST')
            user = os.getenv('REDSHIFT_USERNAME')
            password = os.getenv('REDSHIFT_PASSWORD')
            database = os.getenv('REDSHIFT_DBNAME')
            puerto = os.getenv('REDSHIFT_PORT')

            conn_engine = f'postgresql://{user}:{password}@{host}:{puerto}/{database}'
            engine = create_engine(conn_engine)
            logging.info("Conexión a PostgreSQL exitosa.")
            return engine
        except Exception as e:
            logging.error(f"Error al conectar con PostgreSQL: {e}")
            return None

    @staticmethod
    def conexion_redshift():
        try:
            host = os.getenv('REDSHIFT_HOST')
            user = os.getenv('REDSHIFT_USERNAME')
            password = os.getenv('REDSHIFT_PASSWORD')
            database = os.getenv('REDSHIFT_DBNAME')
            puerto = os.getenv('REDSHIFT_PORT')

            conn_engine = f'redshift+psycopg2://{user}:{password}@{host}:{puerto}/{database}'
            engine = create_engine(conn_engine)
            logging.info("Conexión a AWS Redshift exitosa.")
            return engine
        except Exception as e:
            logging.error(f"Error al conectar con AWS Redshift: {e}")
            return None
