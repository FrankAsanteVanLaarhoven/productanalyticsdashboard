from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine

def get_postgres_conn():
    return create_engine('postgresql://airflow:airflow@postgres/airflow')

def check_data_quality(**context):
    """Perform comprehensive data quality checks"""
    engine = get_postgres_conn()
    
    # Get latest data
    query = """
    SELECT * FROM meap.amazon_sales 
    WHERE sale_date >= CURRENT_DATE - INTERVAL '1 day'
    """
    df = pd.read_sql(query, engine)
    
    quality_issues = []
    
    # Data type validations
    if not all(df['amount'].apply(lambda x: isinstance(x, (int, float)))):
        quality_issues.append("Invalid amount data types found")
    
    if not all(df['sale_date'].apply(lambda x: isinstance(x, pd.Timestamp))):
        quality_issues.append("Invalid date formats found")
    
    # Null checks
    required_fields = ['category', 'sale_date', 'status', 'amount']
    for field in required_fields:
        null_count = df[field].isnull().sum()
        if null_count > 0:
            quality_issues.append(f"Found {null_count} null values in {field}")
    
    # Value range checks
    if not all(df['amount'] >= 0):
        quality_issues.append("Negative amounts found")
    
    if not all(df['quantity'] > 0):
        quality_issues.append("Invalid quantities found")
    
    # Volume checks
    daily_volume = len(df)
    if daily_volume < 1:  # Adjust threshold as needed
        quality_issues.append(f"Low daily volume: {daily_volume} records")
    
    # Save quality metrics
    quality_metrics = {
        'date': datetime.now().date(),
        'total_records': len(df),
        'null_percentage': df.isnull().mean().mean() * 100,
        'issues_found': len(quality_issues)
    }
    
    pd.DataFrame([quality_metrics]).to_sql(
        'data_quality_metrics', 
        engine, 
        schema='meap', 
        if_exists='append', 
        index=False
    )
    
    if quality_issues:
        raise ValueError(f"Data quality issues found: {quality_issues}")
    
    return "Data quality checks passed"

default_args = {
    'owner': 'favl',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['info@frankvanlaarhoven.co.uk'],
    'email_on_failure': True,
    'retries': 1
}

with DAG(
    'data_quality_checks',
    default_args=default_args,
    description='Data Quality Monitoring',
    schedule_interval='@daily',
    catchup=False
) as dag:

    quality_check = PythonOperator(
        task_id='check_data_quality',
        python_callable=check_data_quality
    )

    notify_success = EmailOperator(
        task_id='notify_success',
        to='info@frankvanlaarhoven.co.uk',
        subject='Data Quality Checks Passed',
        html_content='All data quality checks have passed.'
    )

    quality_check >> notify_success
