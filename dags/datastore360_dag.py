import sys
from datetime import datetime, timezone

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

sys.path.insert(0, "/opt/airflow")

from src import transform


def _extract():
    raw = pd.read_csv('/opt/airflow/data/raw/store_data.csv')
    return raw.to_json(orient='split')


def _transform(ti):
    raw = pd.read_json(ti.xcom_pull(task_ids='extract_data'), orient='split')
    clean = transform.run_pipeline(raw)
    clean.to_csv('/opt/airflow/data/processed/store_data_clean.csv', index=False)


def _load():
    clean = pd.read_csv(
        '/opt/airflow/data/processed/store_data_clean.csv',
        dtype={'Postal Code': str},
    )
    engine = PostgresHook(postgres_conn_id='postgres_datastore').get_sqlalchemy_engine()
    clean.to_sql('store_data', engine, if_exists='replace', index=False)
    engine.dispose()


with DAG(
    dag_id="datastore360",
    start_date=datetime(2026, 9, 18, tzinfo=timezone.utc),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    extract_data = PythonOperator(task_id="extract_data", python_callable=_extract)

    transform_data = PythonOperator(
        task_id="transform_data",
        python_callable=_transform,
    )

    load_data = PythonOperator(
        task_id="load_data",
        python_callable=_load,
    )

    extract_data >> transform_data >> load_data