# /Users/frankvanlaarhoven/airflow_project/dags/amazon_sales_etl/dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.datasets import Dataset
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime, timedelta
import os
import logging

# Use absolute imports
from amazon_sales_etl.operators.extract import extract_sales_data
from amazon_sales_etl.operators.transform import transform_sales_data
from amazon_sales_etl.operators.load import load_sales_data

# Configure logging
logger = logging.getLogger(__name__)

# Define datasets
PRODUCT_RECOMMENDATIONS = Dataset("meap/product_recommendations")

# SQL statements
CREATE_SCHEMA_SQL = "CREATE SCHEMA IF NOT EXISTS meap;"

CREATE_SALES_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS meap.sales_data (
    sku_code VARCHAR(50) PRIMARY KEY,
    design_no VARCHAR(50) NOT NULL,
    stock INTEGER NOT NULL CHECK (stock >= 0),
    category VARCHAR(50) NOT NULL,
    size VARCHAR(20) NOT NULL,
    color VARCHAR(30) NOT NULL,
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    qty INTEGER NOT NULL CHECK (qty >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_design UNIQUE (design_no)
);

-- Add trigger to update timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS update_sales_data_updated_at ON meap.sales_data;

CREATE TRIGGER update_sales_data_updated_at
    BEFORE UPDATE ON meap.sales_data
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
"""

CREATE_RATINGS_VIEW_SQL = """
CREATE OR REPLACE VIEW meap.vw_product_ratings AS
SELECT 
    sku_code,
    design_no,
    stock,
    category,
    size,
    color,
    amount as avg_price,
    qty as total_units,
    created_at,
    updated_at,
    CASE 
        WHEN amount >= 70 THEN 'AAA'
        WHEN amount >= 60 THEN 'AA'
        WHEN amount >= 50 THEN 'A'
        ELSE 'B'
    END as price_rating,
    CASE 
        WHEN qty >= 30 THEN 'High Volume'
        WHEN qty >= 25 THEN 'Medium Volume'
        ELSE 'Standard Volume'
    END as volume_rating
FROM meap.sales_data;
"""
CREATE_RECOMMENDATIONS_VIEW_SQL = """
CREATE OR REPLACE VIEW meap.vw_product_recommendations AS
SELECT 
    p.sku_code,
    p.design_no,
    p.stock,
    p.category,
    p.size,
    p.color,
    p.avg_price,
    p.total_units,
    p.created_at,
    p.updated_at,
    p.price_rating,
    p.volume_rating,
    CASE p.price_rating
        WHEN 'AAA' THEN 'Maintain premium pricing'
        WHEN 'AA' THEN 'Consider price optimization'
        WHEN 'A' THEN 'Review pricing strategy'
        ELSE 'Evaluate market position'
    END as price_strategy,
    CASE p.volume_rating
        WHEN 'High Volume' THEN 'Maintain inventory levels'
        WHEN 'Medium Volume' THEN 'Monitor stock levels'
        ELSE 'Review stock strategy'
    END as volume_strategy
FROM meap.vw_product_ratings p;
"""

VERIFY_DATA_SQL = """
WITH metrics AS (
    SELECT 
        COUNT(*) as total_records,
        COUNT(DISTINCT sku_code) as unique_skus,
        COUNT(DISTINCT category) as unique_categories,
        AVG(avg_price) as avg_price,
        AVG(total_units) as avg_units,
        COUNT(CASE WHEN price_rating = 'AAA' THEN 1 END) as premium_products,
        COUNT(CASE WHEN volume_rating = 'High Volume' THEN 1 END) as high_volume_products
    FROM meap.vw_product_recommendations
)
SELECT 
    *,
    CASE 
        WHEN total_records = unique_skus THEN 'PASS'
        ELSE 'FAIL'
    END as sku_uniqueness_check,
    CASE 
        WHEN avg_price > 0 AND avg_units > 0 THEN 'PASS'
        ELSE 'FAIL'
    END as metrics_validity_check
FROM metrics;
"""

def _verify_data_quality(**context):
    """Verify data quality and raise error if checks fail"""
    hook = PostgresHook(postgres_conn_id='postgres_default')
    records = hook.get_records(VERIFY_DATA_SQL)
    
    if records[0][-2] == 'FAIL' or records[0][-1] == 'FAIL':
        raise ValueError("Data quality checks failed!")
    
    logger.info("Data quality checks passed successfully!")
    return True

with DAG(
    'amazon_sales_etl',
    default_args={
        'owner': 'favl',
        'depends_on_past': False,
        'start_date': datetime(2024, 1, 1),
        'email': ['info@frankvanlaarhoven.co.uk'],
        'email_on_failure': True,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
    },
    description='ETL pipeline for Amazon sales data with product recommendations',
    schedule_interval='@daily',
    catchup=False,
    tags=['amazon', 'sales', 'recommendations']
) as dag:

    create_schema = PostgresOperator(
        task_id='create_schema',
        postgres_conn_id='postgres_default',
        sql=CREATE_SCHEMA_SQL
    )

    extract_task = PythonOperator(
        task_id='extract_sales_data',
        python_callable=extract_sales_data,
        provide_context=True
    )

    transform_task = PythonOperator(
        task_id='transform_sales_data',
        python_callable=transform_sales_data,
        provide_context=True
    )

    load_task = PythonOperator(
        task_id='load_sales_data',
        python_callable=load_sales_data,
        provide_context=True
    )

    create_sales_table = PostgresOperator(
        task_id='create_sales_table',
        postgres_conn_id='postgres_default',
        sql=CREATE_SALES_TABLE_SQL
    )

    create_ratings_view = PostgresOperator(
        task_id='create_ratings_view',
        postgres_conn_id='postgres_default',
        sql=CREATE_RATINGS_VIEW_SQL
    )

    create_recommendations_view = PostgresOperator(
        task_id='create_recommendations_view',
        postgres_conn_id='postgres_default',
        sql=CREATE_RECOMMENDATIONS_VIEW_SQL,
        outlets=[PRODUCT_RECOMMENDATIONS]
    )

    verify_data = PythonOperator(
        task_id='verify_data',
        python_callable=_verify_data_quality,
        provide_context=True
    )

    # Set task dependencies
    create_schema >> \
    extract_task >> \
    transform_task >> \
    load_task >> \
    create_sales_table >> \
    create_ratings_view >> \
    create_recommendations_view >> \
    verify_data
