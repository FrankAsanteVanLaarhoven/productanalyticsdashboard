# /Users/frankvanlaarhoven/airflow_project/dags/amazon_sales_etl/operators/extract.py
from airflow.hooks.base import BaseHook
import kaggle
import pandas as pd
import os
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

class DataSourceExtractor(ABC):
    """Base class for data source extractors"""
    
    @abstractmethod
    def extract(self) -> pd.DataFrame:
        pass

class KaggleExtractor(DataSourceExtractor):
    """Extracts data from Kaggle datasets"""
    
    def __init__(self, dataset_name: str, download_path: str):
        self.dataset_name = dataset_name
        self.download_path = download_path
    
    def extract(self) -> pd.DataFrame:
        os.environ['KAGGLE_CONFIG_DIR'] = '/opt/airflow/.kaggle'
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(
            self.dataset_name,
            path=self.download_path,
            unzip=True
        )
        return pd.read_csv(f"{self.download_path}/amazon_products.csv")

class CSVExtractor(DataSourceExtractor):
    """Extracts data from local CSV files"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def extract(self) -> pd.DataFrame:
        return pd.read_csv(self.file_path)

class S3Extractor(DataSourceExtractor):
    """Extracts data from AWS S3"""
    
    def __init__(self, bucket: str, key: str, aws_conn_id: str = 'aws_default'):
        self.bucket = bucket
        self.key = key
        self.aws_conn_id = aws_conn_id
    
    def extract(self) -> pd.DataFrame:
        import s3fs
        aws_conn = BaseHook.get_connection(self.aws_conn_id)
        fs = s3fs.S3FileSystem(
            key=aws_conn.login,
            secret=aws_conn.password
        )
        with fs.open(f"{self.bucket}/{self.key}") as f:
            return pd.read_csv(f)

def get_extractor(source_type: str, **kwargs) -> DataSourceExtractor:
    """Factory function to create appropriate extractor"""
    extractors = {
        'kaggle': KaggleExtractor,
        'csv': CSVExtractor,
        's3': S3Extractor
    }
    return extractors[source_type](**kwargs)

def extract_sales_data(**context) -> str:
    """Extract data from specified source"""
    try:
        # Get source configuration from environment or DAG config
        source_config = context['dag_run'].conf.get('source_config', {
            'type': 'kaggle',
            'dataset_name': 'lokeshparab/amazon-products-dataset',
            'download_path': '/opt/airflow/data'
        })
        
        # Create appropriate extractor
        extractor = get_extractor(**source_config)
        
        # Extract data
        df = extractor.extract()
        
        # Log extraction statistics
        stats = {
            'total_records': len(df),
            'categories': df['category'].nunique(),
            'total_products': df['product_name'].nunique()
        }
        
        # Push to XCom for next task
        context['task_instance'].xcom_push(key='raw_data', value=df.to_dict('records'))
        
        return f"Successfully extracted {len(df)} records"
        
    except Exception as e:
        print(f"Error extracting data: {str(e)}")
        raise