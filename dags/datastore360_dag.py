from datetime import datetime, timezone

from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG(
    dag_id="datastore360",
    start_date=datetime(2026, 9, 18, tzinfo=timezone.utc),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=lambda: None,
    )