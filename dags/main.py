from datetime import datetime
from modules import send_email
from modules import RequestApi

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.bash import BashOperator

def fetch_anime_data():
    api = RequestApi().request_anime()
    return api

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 7, 3),
    'email_on_retry': True,
    'retries': 1,
}

DAG_ID = "postgres_operator_dag"

with DAG(
    dag_id='dag_etl_api',
    default_args=default_args,
    schedule_interval='@daily',
) as dag:

    fetch_anime_task = PythonOperator(
        task_id='fetch_anime_data',
        python_callable=fetch_anime_data,
        provide_context=True
    )

    populate_data = SQLExecuteQueryOperator(
        task_id='insertar_en_tabla',
        sql="""
        truncate table public.lista_anime;

        INSERT INTO public.lista_anime(
            "Titulo_Anime", "Episodios", "Tipo", "Estado")
            VALUES 
                ('anime1', 5, 'xtipo', 'finalizado'),
                ('anime2', 5, 'xtipo', 'finalizado');
        """,
        conn_id="postgres_operator_dag"
    )

    email_massive = PythonOperator(
        task_id="mail_sender",
        python_callable=send_email,
        provide_context=True
    )

    printer_airflow_variables = BashOperator(
        task_id="printer_variables",
        bash_command='echo "{{ var.value.subject_mail }} --> {{ var.value.email }} -> {{ var.value.email_password }}"',
    )

    fetch_anime_task >> populate_data >> printer_airflow_variables >> email_massive
