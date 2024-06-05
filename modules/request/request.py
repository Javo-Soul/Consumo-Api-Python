import requests
import pandas as pd
import json
import logging
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
        self._conexion_postgres = ConexionesSQL.conexion_postgres()

    def request_anime(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            data = response.json()

            animes = {
                'Titulo_Anime': [str(e['title']) for e in data['data']],
                'Episodios': [str(e['episodes']) for e in data['data']],
                'Tipo': [str(e['status']) for e in data['data']],
                'Estado': [str(e['status']) for e in data['data']],
            }

            df = pd.DataFrame(animes)
            df.to_sql('lista_anime', self._conexion_postgres, if_exists='replace', index=False)
            logging.info("Datos guardados exitosamente en la base de datos.")
            return df
        except requests.RequestException as e:
            logging.error(f"Error al realizar la solicitud a la API: {e}")
        except Exception as e:
            logging.error(f"Error procesando los datos: {e}")
