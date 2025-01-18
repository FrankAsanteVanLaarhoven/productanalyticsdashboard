from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def test_function():
    return "Hello from MEAP!"

with DAG(
    'test_dag',
    start_date=datetime(2024, 1, 1),
    schedule_interval=timedelta(days=1),
    catchup=False
) as dag:

    test_task = PythonOperator(
        task_id='test_task',
        python_callable=test_function,
    )
