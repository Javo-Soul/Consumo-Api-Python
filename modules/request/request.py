import requests
import pandas as pd
import json
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, text
from modules.conexionSQL.conexionBD import ConexionesSQL

# Configuración del logging
logging.basicConfig(
    filename='request.log',  # Nombre del archivo de log
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class RequestApi:
    def __init__(self, url: str):
        self.url = url
        try:
            self._conexion_postgres = ConexionesSQL.conexion_postgres()
        except Exception as e:
            logging.error(f"Error al establecer conexión con la base de datos: {e}")
            raise

    def create_table_if_not_exists(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS public.lista_anime
        (
            "Titulo_Anime" text COLLATE pg_catalog."default" NOT NULL,
            "Episodios" text COLLATE pg_catalog."default",
            "Tipo" text COLLATE pg_catalog."default",
            "Estado" text COLLATE pg_catalog."default",
            CONSTRAINT lista_anime_pkey PRIMARY KEY ("Titulo_Anime")
        )
        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.lista_anime
            OWNER to postgres;
        '''
        try:
            with self._conexion_postgres.connect() as connection:
                connection.execute(text(create_table_query))
                logging.info("Tabla 'lista_anime' verificada/creada exitosamente.")
        except SQLAlchemyError as e:
            logging.error(f"Error al crear/verificar la tabla en la base de datos: {e}")
            raise

    def request_anime(self):
        try:
            # Crear la tabla si no existe
            self.create_table_if_not_exists()

            response = requests.get(self.url)
            response.raise_for_status()
            data = response.json()

            animes = {
                'Titulo_Anime': [str(e['title']) for e in data['data']],
                'Episodios': [str(e['episodes']) for e in data['data']],
                'Tipo': [str(e['type']) for e in data['data']],
                'Estado': [str(e['status']) for e in data['data']],
            }

            df = pd.DataFrame(animes)
            df['Titulo_Anime'] = df['Titulo_Anime'].astype(str)
            df['Episodios']    = df['Episodios'].astype(str)
            df['Tipo']         = df['Tipo'].astype(str)
            df['Estado']       = df['Estado'].astype(str)

            # Verificar registros existentes
            existing_titles = pd.read_sql('SELECT "Titulo_Anime" FROM public.lista_anime', self._conexion_postgres)

            # Asegurar que la columna se compara correctamente
            new_data = df[~df['Titulo_Anime'].isin(existing_titles['Titulo_Anime'].astype(str))]

            if not new_data.empty:
                new_data.to_sql('lista_anime', self._conexion_postgres, if_exists='append', index=False)
                logging.info("Nuevos datos guardados exitosamente en la base de datos.")
            else:
                logging.info("No se encontraron nuevos datos para insertar.")
                
            return new_data
        except requests.RequestException as e:
            logging.error(f"Error al realizar la solicitud a la API: {e}")
            return None
        except SQLAlchemyError as e:
            logging.error(f"Error en la base de datos: {e}")
            return None
        except Exception as e:
            logging.error(f"Error procesando los datos: {e}")
            return None
