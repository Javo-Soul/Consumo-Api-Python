import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()


class conexionesSQL:
    def conexionPostgres():
        host     = os.getenv('REDSHIFT_HOST')
        user     = os.getenv('REDSHIFT_USERNAME')
        password = os.getenv('REDSHIFT_PASSWORD')
        database = os.getenv('REDSHIFT_DBNAME')
        puerto   = os.getenv('REDSHIFT_PORT')

        conn_engine = ''

        try:
            conn_engine = f'''postgresql://{user}:{password}@{host}:{puerto}/{database}'''
            conn_engine = create_engine(conn_engine)
        except Exception as e:
            print(e)

        return conn_engine
