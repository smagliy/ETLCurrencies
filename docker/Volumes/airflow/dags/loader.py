import sys
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

EXTRACT_DIR = "/opt/airflow"
if EXTRACT_DIR not in sys.path:
    sys.path.append(EXTRACT_DIR)

from src.services.load.load_service import DailyLoad, HistoricalLoad
from src.services.minio.bucket_service import BucketOperations

minio = BucketOperations(
    os.environ['MINIO_URL'],
    os.environ['MINIO_ACCESS_KEY'],
    os.environ['MINIO_SECRET_KEY']
)


def run_daily_loader():
    DailyLoad(minio_client=minio, bucket_name='exchange').run()


def run_historical_loader():
    HistoricalLoad(minio_client=minio, bucket_name='exchange').run()


# DAILY DAG
with DAG(
    dag_id="daily_exchange_rate_loader",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["exchange", "daily"],
) as daily_dag:

    load_daily = PythonOperator(
        task_id="load_daily_rates",
        python_callable=run_daily_loader,
    )

    load_daily


# MONTHLY HISTORICAL DAG
with DAG(
    dag_id="monthly_historical_exchange_loader",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@monthly",
    catchup=False,
    tags=["exchange", "historical"],
) as historical_dag:

    load_historical = PythonOperator(
        task_id="load_historical_rates",
        python_callable=run_historical_loader,
    )

    load_historical
