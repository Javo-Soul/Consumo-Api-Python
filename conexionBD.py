import os
from sqlalchemy import create_engine

def conexionBD():
    host = os.environ.get('POSTGRESQL_HOST')
    user = os.environ.get('POSTGRESQL_USER')
    password = os.environ.get('POSTGRESQL_PASSWORD')
    database = os.environ.get('POSTGRESQL_DB')
    puerto = 5432

    conn_engine = ''

    try:
        conn_engine = f'''postgresql://{user}:{password}@{host}:{puerto}/{database}'''
        conn_engine = create_engine(conn_engine)
    except Exception as e:
        print(e)

    return conn_engine

print(conexionBD())