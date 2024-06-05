import requests
import pandas as pd
import json
from modules.conexionSQL.conexionBD import conexionesSQL

###############################################
class requestApi():
    def __init__(self, url : str):
        self.url = url
        self._conexionPostgres = conexionesSQL.conexionPostgres()

    def requestAnime(self):
        link = self.url
        data = requests.get(link)
        titulo,episodios,tipo,estado = [],[],[],[]
        conn = self._conexionPostgres
        diccionario = {}

        try:
            if data.status_code == 200:
                data = data.json()

                for e in data['data']:
                    titulo.append(str(e['title']))
                    episodios.append(str(e['episodes']))
                    tipo.append(str(e['status']))
                    estado.append(str(e['status']))

                diccionario.update({'Titulo_Anime':titulo,'Episodios'   :episodios,'tipo':tipo,'estado':estado})

                data = pd.DataFrame.from_dict(diccionario)

                ##### los datos obtenidos de la API se cargan en un csv ########
                data.to_csv('listaanime.csv', sep  = ';',header=True, encoding='UTF-8')

                ##### los datos del csv se cargan en la base de datos ########
                df = pd.read_csv('listaanime.csv',sep=';').to_sql('lista_anime', conn, if_exists= 'replace', index= False)

            else:
                data

            return data
        except Exception as e:
            print(e)
