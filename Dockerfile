FROM apache/airflow:slim-latest-python3.11.5

USER root

RUN apt-get update && apt-get install -y \
    python3-pip \
    && pip3 install --upgrade pip \
    && pip3 install pandas SQLAlchemy psycopg2-binary python-dotenv

USER airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV POSTGRES_HOST=localhost
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=SAuser2025.
ENV POSTGRES_PORT=5433
ENV POSTGRES_DB=postgres
ENV AIRFLOW_UID=197611

# Comando por defecto para ejecutar la aplicación
CMD ["airflow", "webserver","python", "dags/__main__.py"]

