#!/bin/bash
airflow standalone

airflow db migrate

airflow users create \
    --username admin \
    --firstname anderson \
    --lastname oca \
    --role Admin \
    --email javier.carrionv@gmail.com

airflow webserver --port 8081

airflow scheduler