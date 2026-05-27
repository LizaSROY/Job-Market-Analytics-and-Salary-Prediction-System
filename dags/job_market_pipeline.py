from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

# Import functions from project files
from extraction.extract import extract
from transformation.transform import transform
from loading.load import load


# Create DAG
with DAG(
    dag_id="job_market_pipeline",

    start_date=datetime(2025,1,1),

    schedule=None,

    catchup=False

) as dag:


    # Extract task
    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract
    )


    # Transform task
    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform
    )


    # Load task
    load_task = PythonOperator(
        task_id="load",
        python_callable=load
    )


    # Task order
    extract_task >> transform_task >> load_task