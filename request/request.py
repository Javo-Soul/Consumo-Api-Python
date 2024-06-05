import requests
import pandas as pd
import json
from conexionBD import conexionBD

###############################################
class requestApi():
    def __init__(self, url : str):
        self.url = url

    def requestAnime(self):
        link = self.url
        data = requests.get(link)
        titulo,episodios,tipo,estado = [],[],[],[]
        conn = conexionBD()
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
                data.to_csv('listaanime.csv', sep  = ';',header=True, encoding='UTF-8')

                # df = pd.read_csv('listaanime.csv').to_sql('lista_anime', conn, if_exists= 'replace', index= False)

            else:
                data

            return data
        except Exception as e:
            print(e)
