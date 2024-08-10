import os
import requests
import pandas as pd
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, text
from modules.conexionSQL.conexionBD import ConexionesSQL
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import unicodedata

load_dotenv()

# Configuración del logging
logging.basicConfig(
    filename='request.log',  # Nombre del archivo de log
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class RequestApi:
    def __init__(self, api:str = "https://api.jikan.moe/v4/top/anime"):            
        self.urlTop = api 
        self._conexion_server = ConexionesSQL.conexion_redshift()

    def create_table_if_not_exists(self):
        create_table_lista = '''
        CREATE TABLE IF NOT EXISTS public.lista_anime
        (
            Titulo_Anime VARCHAR(255) PRIMARY KEY,
            Episodios varchar(5),
            Tipo VARCHAR(40),
            Estado VARCHAR(40)
        );
        '''

        create_table_canciones = '''
        CREATE TABLE IF NOT EXISTS public.lista_anime_canciones
        (
            name VARCHAR(200) PRIMARY KEY,
            artist VARCHAR(200),
            popularity VARCHAR(200)
        )
        '''
        try:
            with self._conexion_server.connect() as connection:
                connection.execute(text(create_table_lista))
                logging.info("Tabla 'lista_anime' verificada/creada exitosamente.")

            with self._conexion_server.connect() as connection:
                connection.execute(text(create_table_canciones))
                logging.info("Tabla 'canciones_anime' verificada/creada exitosamente.")

        except SQLAlchemyError as e:
            logging.error(f"Error al crear/verificar la tabla en la base de datos: {e}")

    def normalize_text(self, text):
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

    def request_anime(self):
        try:
            self.create_table_if_not_exists()

            response = requests.get(self.urlTop)
            response.raise_for_status()
            data = response.json()

            animes = {
                'Titulo_Anime': [self.normalize_text(str(e['title'])) for e in data['data']],
                'Episodios': [str(e['episodes']) for e in data['data']],
                'Tipo': [str(e['type']) for e in data['data']],
                'Estado': [str(e['status']) for e in data['data']],
            }

            df = pd.DataFrame(animes)
            df['Titulo_Anime'] = df['Titulo_Anime'].astype(str)
            df['Episodios']    = df['Episodios'].astype(str)
            df['Tipo']         = df['Tipo'].astype(str)
            df['Estado']       = df['Estado'].astype(str)

            # df = df.head(17)
            # df.to_csv('lista.txt')

            existing_titles = pd.read_sql('SELECT Titulo_Anime FROM public.lista_anime', self._conexion_server)
            new_data = df[~df['Titulo_Anime'].isin(existing_titles['titulo_anime'].astype(str))]

            if not new_data.empty:
                new_data.to_sql('lista_anime', self._conexion_server, if_exists='append', index=False)
                logging.info("Nuevos datos guardados exitosamente en la base de datos.")
            else:
                logging.info("No se encontraron nuevos datos para insertar.")
                
            return new_data

        except requests.RequestException as e:
            logging.error(f"Error al realizar la solicitud a la API: {e}")
        except SQLAlchemyError as e:
            logging.error(f"Error en la base de datos: {e}")
        except Exception as e:
            logging.error(f"Error procesando los datos: {e}")

    def request_top_spo(self):
        idSpotify     =  os.getenv('cliidSpotify')
        idSpotifyPass = os.getenv('clisecretSpotify')
        try:
            self.create_table_if_not_exists()
            client_credentials_manager = SpotifyClientCredentials(client_id=idSpotify, client_secret=idSpotifyPass)
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

            playlist_id = '3Pya3YfwFtuufFDahbfjkI'
            results = sp.playlist_tracks(playlist_id)

            # Extraer información de las canciones
            tracks = results['items']
            top_tracks = []

            for track in tracks:
                track_info = track['track']
                top_tracks.append({
                    'name': self.normalize_text(track_info['name']),
                    'artist': self.normalize_text(track_info['artists'][0]['name']),
                    'popularity': track_info['popularity']
                })

            # Ordenar por popularidad
            top_tracks = sorted(top_tracks, key=lambda x: x['popularity'], reverse=True)

            # Convertir a DataFrame
            df_top_tracks = pd.DataFrame(top_tracks)
            # Mostrar el DataFrame
            existing_titles = pd.read_sql('SELECT "name" FROM public.lista_anime_canciones', self._conexion_server)            
            new_data = df_top_tracks[~df_top_tracks['name'].isin(existing_titles['name'].astype(str))]

            if not new_data.empty:
                new_data.to_sql('lista_anime_canciones', self._conexion_server, if_exists='append', index=False)
                logging.info("Nuevos datos guardados exitosamente en la base de datos.")
            else:
                logging.info("No se encontraron nuevos datos para insertar.")

        except requests.RequestException as e:
              logging.error(f"Error al realizar la solicitud a la API: {e}")
        except SQLAlchemyError as e:
              logging.error(f"Error en la base de datos: {e}")
        except Exception as e:
              logging.error(f"Error procesando los datos: {e}")
