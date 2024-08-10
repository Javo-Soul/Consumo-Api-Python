from datetime import datetime
from modules import send_email
from modules import RequestApi

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.bash import BashOperator

def fetch_lista_anime():
    apiTop     = RequestApi().request_anime()
    return apiTop

def fetch_lista_canciones():
    apiSpotify = RequestApi().request_top_spo()
    return apiSpotify 

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

    fetch_anime_lista = PythonOperator(
        task_id='fetch_anime_data',
        python_callable=fetch_lista_anime,
        provide_context=True
    )

    fetch_anime_spotify = PythonOperator(
        task_id='fetch_anime_canciones',
        python_callable=fetch_lista_canciones,
        provide_context=True
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

    fetch_anime_lista >> fetch_anime_spotify >> printer_airflow_variables >> email_massive
