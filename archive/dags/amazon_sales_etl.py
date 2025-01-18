from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, timedelta
import pandas as pd
import kagglehub
import os
import logging
from sqlalchemy import create_engine, text
import numpy as np
from typing import List, Dict, Any
import json

# Enhanced logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataValidator:
    @staticmethod
    def validate_data(df: pd.DataFrame, required_columns: List[str]) -> bool:
        """Enhanced data validation with detailed checks"""
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        if df.empty:
            raise ValueError("Dataframe is empty")
        
        # Additional data quality checks
        null_counts = df[required_columns].isnull().sum()
        if null_counts.any():
            logger.warning(f"Null values found in columns: {null_counts[null_counts > 0]}")
        
        # Data type validation
        numeric_cols = ['selling_price', 'quantity']
        for col in numeric_cols:
            if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
                logger.warning(f"Column {col} is not numeric type")
        
        return True

def extract_sales_data(**context) -> str:
    """Enhanced data extraction with retry mechanism and detailed logging"""
    logger.info("Starting data extraction process...")
    try:
        # Configure Kaggle credentials
        os.environ['KAGGLE_USERNAME'] = context['dag_run'].conf.get('kaggle_username', 'default_username')
        os.environ['KAGGLE_KEY'] = context['dag_run'].conf.get('kaggle_key', 'default_key')
        
        path = kagglehub.dataset_download(
            "thedevastator/amazon-sales-dataset",
            force=True
        )
        
        # Enhanced file handling
        csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
        if not csv_files:
            raise FileNotFoundError("No CSV files found in downloaded dataset")
        
        file_path = os.path.join(path, csv_files[0])
        df = pd.read_csv(file_path, low_memory=False)
        
        # Enhanced validation
        required_columns = ['category', 'selling_price', 'quantity']
        DataValidator.validate_data(df, required_columns)
        
        # Data statistics logging
        stats = {
            'total_records': len(df),
            'unique_categories': df['category'].nunique(),
            'price_range': f"{df['selling_price'].min():.2f} - {df['selling_price'].max():.2f}",
            'total_quantity': df['quantity'].sum()
        }
        logger.info(f"Data statistics: {json.dumps(stats, indent=2)}")
        
        # Store raw data with metadata
        context['task_instance'].xcom_push(key='raw_data', value=df.to_dict('records'))
        context['task_instance'].xcom_push(key='data_stats', value=stats)
        
        return f"Successfully extracted {len(df)} records with {df['category'].nunique()} unique categories"
    
    except Exception as e:
        logger.error(f"Extraction failed: {str(e)}", exc_info=True)
        raise

def transform_sales_data(**context) -> str:
    """Enhanced data transformation with advanced analytics"""
    logger.info("Starting data transformation process...")
    try:
        raw_data = context['task_instance'].xcom_pull(task_ids='extract_sales_data', key='raw_data')
        if not raw_data:
            raise ValueError("No raw data available from extraction step")
        
        df = pd.DataFrame(raw_data)
        
        # Enhanced data cleaning
        df['selling_price'] = pd.to_numeric(df['selling_price'], errors='coerce')
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
        
        # Remove outliers
        for col in ['selling_price', 'quantity']:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            df = df[~((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR)))]
        
        # Advanced aggregation
        transformed_df = df.groupby('category').agg({
            'selling_price': ['mean', 'median', 'std'],
            'quantity': ['sum', 'mean', 'count']
        }).reset_index()
        
        # Flatten column names
        transformed_df.columns = ['category', 'amount', 'median_price', 'price_std', 
                                'qty', 'avg_qty', 'transaction_count']
        
        # Calculate additional metrics
        transformed_df['price_volatility'] = transformed_df['price_std'] / transformed_df['amount']
        transformed_df['volume_intensity'] = transformed_df['qty'] / transformed_df['transaction_count']
        
        # Data quality checks
        if transformed_df[['amount', 'qty']].isnull().any().any():
            raise ValueError("Transformed data contains null values")
        
        # Store transformed data with metadata
        context['task_instance'].xcom_push(key='transformed_data', value=transformed_df.to_dict('records'))
        
        return f"Transformed {len(transformed_df)} categories with advanced metrics"
    
    except Exception as e:
        logger.error(f"Transformation failed: {str(e)}", exc_info=True)
        raise

def load_sales_data(**context) -> str:
    """Enhanced data loading with transaction management and verification"""
    logger.info("Starting data load process...")
    engine = None
    try:
        transformed_data = context['task_instance'].xcom_pull(task_ids='transform_sales_data', key='transformed_data')
        if not transformed_data:
            raise ValueError("No transformed data available for loading")
        
        df = pd.DataFrame(transformed_data)
        logger.info(f"Preparing to load {len(df)} records")
        
        engine = create_engine('postgresql://airflow:airflow@postgres/airflow')
        
        with engine.begin() as connection:
            # Ensure schema exists
            connection.execute(text("CREATE SCHEMA IF NOT EXISTS meap;"))
            
            # Backup existing data
            connection.execute(text(
                "CREATE TABLE IF NOT EXISTS meap.sales_data_backup AS SELECT * FROM meap.sales_data"
            ))
            
            # Clear existing data
            connection.execute(text("TRUNCATE TABLE meap.sales_data"))
            
            # Load new data
            df.to_sql(
                'sales_data',
                connection,
                schema='meap',
                if_exists='append',
                index=False,
                method='multi',
                chunksize=1000
            )
            
            # Verify data load
            result = connection.execute(text(
                "SELECT COUNT(*), AVG(amount), SUM(qty) FROM meap.sales_data"
            ))
            stats = result.fetchone()
            
            if stats[0] != len(df):
                raise ValueError(f"Data load mismatch. Expected {len(df)} records, loaded {stats[0]}")
            
            # Log load statistics
            logger.info(f"Load statistics: {stats}")
            
        return f"Successfully loaded {stats[0]} records with avg price ${stats[1]:.2f} and total quantity {stats[2]}"
    
    except Exception as e:
        logger.error(f"Load failed: {str(e)}", exc_info=True)
        raise
    finally:
        if engine:
            engine.dispose()

# Enhanced DAG configuration
default_args = {
    'owner': 'favl',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['info@frankvanlaarhoven.co.uk'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(minutes=30),
    'on_failure_callback': lambda context: logger.error(f"Task failed: {context['task_instance'].task_id}")
}

# Create DAG with enhanced configuration
with DAG(
    'amazon_sales_etl',
    default_args=default_args,
    description='Enhanced ETL pipeline for Amazon sales data with advanced analytics',
    schedule_interval='@daily',
    catchup=False,
    tags=['amazon', 'sales', 'etl'],
    max_active_runs=1
) as dag:

    # Extract task with enhanced configuration
    extract_task = PythonOperator(
        task_id='extract_sales_data',
        python_callable=extract_sales_data,
        retries=3,
        retry_delay=timedelta(minutes=2),
        execution_timeout=timedelta(minutes=10),
        provide_context=True
    )

    # Transform task with enhanced configuration
    transform_task = PythonOperator(
        task_id='transform_sales_data',
        python_callable=transform_sales_data,
        retries=2,
        retry_delay=timedelta(minutes=2),
        execution_timeout=timedelta(minutes=10),
        provide_context=True
    )

    # Load task with enhanced configuration
    load_task = PythonOperator(
        task_id='load_sales_data',
        python_callable=load_sales_data,
        retries=2,
        retry_delay=timedelta(minutes=2),
        execution_timeout=timedelta(minutes=10),
        provide_context=True
    )

    # Create product ratings view
    create_ratings_view = PostgresOperator(
        task_id='create_ratings_view',
        postgres_conn_id='postgres_default',
        sql="""
        CREATE OR REPLACE VIEW meap.vw_product_ratings AS
        SELECT 
            category,
            amount as avg_price,
            qty as total_units,
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
    )

    # Create recommendations view
    create_recommendations_view = PostgresOperator(
        task_id='create_recommendations_view',
        postgres_conn_id='postgres_default',
        sql="""
        CREATE OR REPLACE VIEW meap.vw_product_recommendations AS
        SELECT 
            p.*,
            CASE price_rating
                WHEN 'AAA' THEN 'Maintain premium pricing'
                WHEN 'AA' THEN 'Consider price optimization'
                WHEN 'A' THEN 'Review pricing strategy'
                ELSE 'Evaluate market position'
            END as price_strategy,
            CASE volume_rating
                WHEN 'High Volume' THEN 'Maintain inventory levels'
                WHEN 'Medium Volume' THEN 'Monitor stock levels'
                ELSE 'Review stock strategy'
            END as volume_strategy
        FROM meap.vw_product_ratings p;
        """
    )

    # Set task dependencies with enhanced logging
    extract_task >> transform_task >> load_task >> create_ratings_view >> create_recommendations_view

    # Log DAG completion
    logger.info("DAG configuration completed successfully")