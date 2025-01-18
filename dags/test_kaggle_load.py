from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import kagglehub
import pandas as pd
import os
import logging

def test_kaggle_download(**context):
    """Test Kaggle dataset download"""
    logging.info("Starting Kaggle test download...")
    
    try:
        # Print environment variables (without sensitive data)
        logging.info(f"KAGGLE_USERNAME set: {bool(os.getenv('KAGGLE_USERNAME'))}")
        logging.info(f"KAGGLE_KEY set: {bool(os.getenv('KAGGLE_KEY'))}")
        
        # Download dataset
        path = kagglehub.dataset_download(
            "thedevastator/unlock-profits-with-e-commerce-sales-data"
        )
        logging.info(f"Dataset downloaded to: {path}")
        
        # List directory contents
        files = os.listdir(path)
        logging.info(f"Files in directory: {files}")
        
        # Find CSV files
        csv_files = [f for f in files if f.endswith('.csv')]
        if not csv_files:
            raise FileNotFoundError("No CSV files found")
            
        # Read first CSV file
        file_path = os.path.join(path, csv_files[0])
        df = pd.read_csv(file_path)
        
        # Print dataset info
        logging.info(f"\nDataset Info:")
        logging.info(f"Total Records: {len(df)}")
        logging.info(f"Columns: {df.columns.tolist()}")
        logging.info(f"\nFirst 5 rows:")
        logging.info(df.head())
        
        return "Kaggle test completed successfully"
        
    except Exception as e:
        logging.error(f"Test failed: {str(e)}")
        raise

default_args = {
    'owner': 'favl',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['info@frankvanlaarhoven.co.uk'],
    'email_on_failure': True,
    'retries': 1
}

with DAG(
    'test_kaggle_load',
    default_args=default_args,
    description='Test Kaggle Dataset Loading',
    schedule_interval=None,
    catchup=False
) as dag:

    test_task = PythonOperator(
        task_id='test_kaggle_download',
        python_callable=test_kaggle_download
    )
