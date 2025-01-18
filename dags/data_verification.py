from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import os
from sqlalchemy import create_engine
import humanize

def get_postgres_conn():
    return create_engine('postgresql://airflow:airflow@postgres/airflow')

def verify_data_stats(**context):
    """Check data statistics and volumes"""
    # Check downloaded files
    data_dir = "/opt/airflow/data"
    file_stats = []
    
    print("\n=== Downloaded Files ===")
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path)
            modified = datetime.fromtimestamp(os.path.getmtime(file_path))
            
            stats = {
                'file': file,
                'size': humanize.naturalsize(size),
                'modified': modified,
                'path': file_path
            }
            file_stats.append(stats)
            print(f"\nFile: {file}")
            print(f"Size: {stats['size']}")
            print(f"Modified: {stats['modified']}")
            print(f"Path: {stats['path']}")
            
            # If CSV, show data preview
            if file.endswith('.csv'):
                df = pd.read_csv(file_path)
                print(f"\nData Preview:")
                print(f"Rows: {len(df)}")
                print(f"Columns: {len(df.columns)}")
                print("\nColumn Names:")
                print(df.columns.tolist())
                print("\nSample Data:")
                print(df.head())
                print("\nData Types:")
                print(df.dtypes)
    
    # Check database stats
    engine = get_postgres_conn()
    
    print("\n=== Database Statistics ===")
    query = """
    SELECT 
        COUNT(*) as total_records,
        MIN(sale_date) as earliest_date,
        MAX(sale_date) as latest_date,
        COUNT(DISTINCT category) as unique_categories,
        COUNT(DISTINCT sku) as unique_skus
    FROM meap.amazon_sales
    """
    
    db_stats = pd.read_sql(query, engine)
    print("\nDatabase Records:")
    print(db_stats)
    
    # Get size of database table
    query = """
    SELECT 
        pg_size_pretty(pg_total_relation_size('meap.amazon_sales')) as table_size,
        pg_size_pretty(pg_indexes_size('meap.amazon_sales')) as index_size
    """
    
    size_stats = pd.read_sql(query, engine)
    print("\nTable Size Information:")
    print(size_stats)
    
    return "Data verification completed"

default_args = {
    'owner': 'favl',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['info@frankvanlaarhoven.co.uk'],
    'email_on_failure': True,
    'retries': 1
}

with DAG(
    'data_verification',
    default_args=default_args,
    description='Verify Data Statistics',
    schedule_interval=None,  # Manual trigger only
    catchup=False
) as dag:

    verify_task = PythonOperator(
        task_id='verify_data_stats',
        python_callable=verify_data_stats
    )
